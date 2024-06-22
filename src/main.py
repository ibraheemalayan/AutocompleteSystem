from random import randint
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from functions import predict_top_words, predict_word_completion

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
