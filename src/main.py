from random import randint
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from functions import predict_top_words, predict_word_completion


# # sample suggestions for all letters
# suggestions = [
#     "أمل",
#     "أخضر",
#     "أرض",
#     "باب",
#     "بحر",
#     "برنامج",
#     "تفاحة",
#     "تمر",
#     "تلفزيون",
#     "ثعلب",
#     "ثوب",
#     "ثقافة",
#     "جامعة",
#     "جبل",
#     "جوال",
#     "حقيبة",
#     "حصان",
#     "حليب",
#     "خروف",
#     "خبز",
#     "خضار",
#     "دواء",
#     "دفتر",
#     "دراجة",
#     "ذئب",
#     "ذهب",
#     "ذرة",
#     "رأس",
#     "رمضان",
#     "ريشة",
#     "زهرة",
#     "زيتون",
#     "زجاج",
#     "ساعة",
#     "سماء",
#     "سيارة",
#     "شمس",
#     "شجرة",
#     "شارع",
#     "صديق",
#     "صحراء",
#     "صندوق",
#     "ضابط",
#     "ضوء",
#     "ضيف",
#     "طاولة",
#     "طائرة",
#     "طبق",
#     "ظرف",
#     "ظبي",
#     "ظلام",
#     "عين",
#     "عصفور",
#     "علم",
#     "غرفة",
#     "غزال",
#     "غذاء",
#     "فراشة",
#     "فندق",
#     "فنجان",
#     "قطار",
#     "قمر",
#     "قلم",
#     "كتاب",
#     "كرسي",
#     "كمبيوتر",
#     "ليمون",
#     "لبن",
#     "لعبة",
#     "ماء",
#     "مدرسة",
#     "موبايل",
#     "نهر",
#     "نجمة",
#     "نافذة",
#     "هواء",
#     "هدية",
#     "هاتف",
#     "وردة",
#     "وطن",
#     "وقت",
#     "يوم",
#     "يد",
#     "يمين",
# ]


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

    predicted_words = predict_top_words(text_input.current_text)

    return {"options": predicted_words}


@app.post("/complete_word")
def complete_word(text_input: TextInput):

    words = text_input.current_text.split()

    if len(words) == 0:
        return {"options": []}

    last_word = words[-1]

    previous_text = " ".join(words[:-1])

    suggestions = predict_word_completion(last_word, previous_text)

    return {"options": suggestions}


# @app.post("/test_trie")
# def test_ltsm(text_input: TextInput):
#     words = text_input.current_text.split()
#     last_word = words[-1] if words else ""


#     predict_top_five_words(model, tokenizer, x)

#     all_suggestions = trie.autocomplete(last_word)

#     if not all_suggestions:
#         return {"options": []}

#     #

#     # # Very basic suggestion based on starting letters (replace with your logic)
#     # s = ["كلمة"]
#     # # add 6 random words from suggestions to s
#     # for i in range(6):
#     #     # random index
#     #     index = randint(0, len(suggestions) - 1)
#     #     s.append(suggestions[index])

#     return {"options": }

# @app.post("/test_trie")
# def test_trie(text_input: TextInput):
#     words = text_input.current_text.split()
#     last_word = words[-1] if words else ""

#     all_suggestions = trie.autocomplete(last_word)

#     if not all_suggestions:
#         return {"options": []}

#     #

#     # # Very basic suggestion based on starting letters (replace with your logic)
#     # s = ["كلمة"]
#     # # add 6 random words from suggestions to s
#     # for i in range(6):
#     #     # random index
#     #     index = randint(0, len(suggestions) - 1)
#     #     s.append(suggestions[index])

#     return {"options": }
