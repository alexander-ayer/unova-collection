from connection import get_connection
from fastapi import FastAPI
from cards_db import get_all_cards
from models import Card

app = FastAPI()

@app.get("/cards", response_model=list[Card])
def list_cards():
    return get_all_cards()