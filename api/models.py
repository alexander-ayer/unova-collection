from typing import Literal
from pydantic import BaseModel

Rarity = Literal['C', 'U', 'R', 'RR', 'RH', 'PB', 'MB', 'IR', 'UR', 'SIR', 'BWR']
CardType = Literal['Grass', 'Fire', 'Water', 'Lightning', 'Psychic', 'Fighting', 'Darkness', 'Metal', 'Dragon', 'Colorless']


class Card(BaseModel):
    card_id: int
    unova_dex_number: int
    pokemon_name: str
    card_number: str
    card_set: str
    card_type: CardType
    rarity: Rarity
    acquired: bool