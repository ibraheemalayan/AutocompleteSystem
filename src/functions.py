from random import randint
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


import tensorflow as tf

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.metrics import top_k_categorical_accuracy

from collections import defaultdict

from os import path, getcwd

import numpy as np

import pickle

base_dir = path.join(getcwd(), "model")


NUMBER_OF_RESULTS = 10

# ############################################################ #
# ############################################################ #
# ############################################################ #


class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end_of_word = False
        self.frequency = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, frequency=1):
        node = self.root
        for char in word:
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency += frequency

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def autocomplete(self, prefix):
        node = self.search(prefix)
        if not node:
            return []

        results = []
        self._dfs(node, prefix, results)
        results.sort(key=lambda x: -x[1])  # Sort by frequency
        return [word for word, freq in results]

    def _dfs(self, node, prefix, results):
        if node.is_end_of_word:
            results.append((prefix, node.frequency))
        for char, next_node in node.children.items():
            self._dfs(next_node, prefix + char, results)

    def update(self, word, frequency=1):
        self.insert(word, frequency)


# ############################################################ #
# ############################################################ #
# ############################################################ #


class CustomUnpickler(pickle.Unpickler):

    def find_class(self, module, name):
        if name == "Trie":
            return Trie
        elif name == "TrieNode":
            return TrieNode
        return super().find_class(module, name)


# ############################################################ #
# ############################################################ #
# ############################################################ #


def top_3_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=3)


def top_5_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=5)


def perplexity(y_true, y_pred):
    cross_entropy = tf.keras.losses.categorical_crossentropy(y_true, y_pred)
    perplexity = tf.exp(cross_entropy)
    return tf.reduce_mean(perplexity)


def load_models():
    ltsm_model = tf.keras.models.load_model(
        path.join(base_dir, "ltsm", "ar_model.keras"),
        custom_objects={
            "top_3_accuracy": top_3_accuracy,
            "top_5_accuracy": top_5_accuracy,
            "perplexity": perplexity,
        },
    )

    with open(path.join(base_dir, "ltsm", "ar_tokenizer.pkl"), "rb") as tokenizer_file:
        tokenizer = CustomUnpickler(tokenizer_file).load()

    with open(path.join(base_dir, "trie", "ar_trie.pkl"), "rb") as trie_file:
        trie = CustomUnpickler(trie_file).load()

    return ltsm_model, tokenizer, trie


# ############################################################ #
# ############################################################ #
# ############################################################ #

ar_model, ar_tokenizer, trie = load_models()


def predict_top_words(seed_text, number_of_results=NUMBER_OF_RESULTS):

    token_list = ar_tokenizer.texts_to_sequences([seed_text])[0]

    MAX_WORDS_IN_CONTEXT = 20 - 1

    padded_token_list = pad_sequences([token_list], maxlen=MAX_WORDS_IN_CONTEXT, padding="pre")

    predicted_words = ar_model.predict(padded_token_list, verbose=0)[0]
    top_indexes = np.argsort(predicted_words)[::-1][:number_of_results]

    top_words = []

    for index in top_indexes:
        for word, idx in ar_tokenizer.word_index.items():
            if idx == index:
                top_words.append(word)
                break

    return top_words


def predict_word_completion(prefix: str, previous_text: str):
    prefix_suggestions = trie.autocomplete(prefix)
    if not prefix_suggestions:
        return []

    if len(previous_text) < 2:
        return prefix_suggestions[:NUMBER_OF_RESULTS]

    # predict next word
    next_word_from_prevs_txt = predict_top_words(previous_text, 40)

    # the words that appeared in both lists are the suggestions
    suggestions = list(set(prefix_suggestions).intersection(next_word_from_prevs_txt))

    len_suggestions = len(suggestions)

    if len_suggestions <= NUMBER_OF_RESULTS:
        return suggestions + prefix_suggestions[: NUMBER_OF_RESULTS - len_suggestions]
    else:
        return suggestions[:NUMBER_OF_RESULTS]
