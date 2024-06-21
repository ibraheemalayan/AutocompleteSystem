from random import randint
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# sample suggestions for all letters
suggestions = [
    "apple",
    "address",
    "banana",
    "ball",
    "cat",
    "car",
    "dog",
    "door",
    "elephant",
    "egg",
    "fish",
    "frog",
    "grape",
    "goat",
    "hat",
    "house",
    "ice",
    "ink",
    "jacket",
    "jelly",
    "kite",
    "key",
    "lion",
    "lemon",
    "mango",
    "monkey",
    "nest",
    "note",
    "orange",
    "owl",
    "parrot",
    "pen",
    "queen",
    "quilt",
    "rat",
    "rose",
    "sun",
    "star",
    "tree",
    "tiger",
    "umbrella",
    "van",
    "vase",
    "water",
    "watch",
    "xylophone",
    "x-ray",
    "yak",
    "yacht",
    "zebra",
    "zoo",
]


app = FastAPI()
templates = Jinja2Templates(directory="frontend")
app.mount("/static", StaticFiles(directory="static"), name="static")


class TextInput(BaseModel):
    current_text: str


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})  # Render index.html


# serve /script.js


@app.post("/predict_next_word")
def predict_next_word(text_input: TextInput):
    words = text_input.current_text.split()
    last_word = words[-1] if words else ""

    # Very basic suggestion based on starting letters (replace with your logic)
    s = ["new word"]
    # add 6 random words from suggestions to s
    for i in range(6):
        # random index
        index = randint(0, len(suggestions) - 1)
        s.append(suggestions[index])

    return {"options": s}


@app.post("/complete_word")
def complete_word(text_input: TextInput):

    words = text_input.current_text.split()

    if len(words) == 0:
        return {"options": []}

    last_word = words[-1]

    # Very basic suggestion based on starting letters (replace with your logic)

    filtered = [w for w in suggestions if w.startswith(last_word)]

    # Similar to predict_next_word (replace with your logic)
    return {"options": filtered[:5]}  # Limit to 5 suggestions
