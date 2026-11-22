from fastapi import FastAPI, Query
from cards_db import get_cards
from models import Card, Rarity, CardSet

app = FastAPI()

@app.get("/cards", response_model=list[Card])
def list_cards(
    card_set: CardSet | None = None,
    rarity: list[Rarity] | None = Query(None),
    acquired: bool | None = None,
    name: str | None = None,
):
    return get_cards(
        card_set=card_set,
        rarity=rarity,
        acquired=acquired,
        name=name,
    )