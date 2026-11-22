from connection import get_connection
from fastapi import FastAPI
from api.cards_db import get_all_cards

app = FastAPI()

@app.get("/cards")
def list_cards():
    return get_all_cards()