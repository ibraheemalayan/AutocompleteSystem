from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# sample suggestions for all letters
suggestions = [
    "apple",
    "banana",
    "cat",
    "dog",
    "elephant",
    "fish",
    "grape",
    "hat",
    "ice",
    "jacket",
    "kite",
    "lion",
    "mango",
    "nest",
    "orange",
    "parrot",
    "queen",
    "rose",
    "sun",
    "tiger",
    "umbrella",
    "van",
    "watch",
    "xylophone",
    "yak",
    "zebra",
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
    suggestions = ["apple", "banana", "orange", "grape"]
    return {"options": suggestions}


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
