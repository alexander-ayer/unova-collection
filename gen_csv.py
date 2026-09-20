import json
import csv
from typing import TypedDict

class CardRow(TypedDict):
    unova_dex_number: int
    pokemon_name: str
    rarity: str
    card_set: str
    card_number: str
    card_type: str
    acquired: int

RARITY_MAP = {
    "Common" : "C",
    "Uncommon" : "U",
    "Rare" : "R",
    "Double Rare" : "RR",
    "Ultra Rare" : "UR",
    "Illustration Rare" : "IR",
    "Special Illustration Rare" : "SIR",
    "Black White Rare" : "BWR"
}

def format_setnum(raw_number, total):
    formatted_string = f"{str(raw_number).zfill(3)}/{str(total).zfill(3)}"
    return formatted_string

def format_rarity(rarity):
    if rarity not in RARITY_MAP:
        raise ValueError(f"Unmapped rarity encountered: {rarity!r}")
    return RARITY_MAP[rarity]

def gen_variants(row):
    rarity = row["rarity"]
    if rarity not in ("C", "U", "R"):
        return [row]
    variants = ["RH", "PB", "MB"]
    new_rows = [row]
    for code in variants:
        new_row = {**row, "rarity": code}
        new_rows.append(new_row)
    return new_rows

def build_row(card):
    dex_number = card["nationalPokedexNumbers"][0] - 494
    name = card["name"]
    rarity = format_rarity(card["rarity"])
    card_number = format_setnum(card["number"], 86)
    if "zsv10pt5" in card["id"]:
        card_set = "BLK"
    elif "rsv10pt5" in card["id"]:
        card_set = "WHT"
    else:
        raise ValueError("Set Cannot be Identified.")
    card_type = card["types"][0]

    row: CardRow = {
        "unova_dex_number" : dex_number,
        "pokemon_name" : name,
        "rarity" : rarity,
        "card_set" : card_set,
        "card_number" : card_number,
        "card_type" : card_type,
        "acquired" : 0   
    }
    return row

def build_rows(filepaths):
    all_rows = []
    for filepath in filepaths:
        with open(filepath, encoding="utf-8") as f:
            cards = json.load(f)
        for card in cards:
            if card["supertype"] != "Pokémon":
                continue
            row = build_row(card)
            variants = gen_variants(row)
            all_rows.extend(variants)
    return all_rows

data_rows = build_rows(["./data/zsv10pt5.json", "./data/rsv10pt5.json"])

SECRET_RARITIES = ("IR", "SIR", "BWR")

def binder_sort_key(row):
    is_secret = row["rarity"] in SECRET_RARITIES
    return (is_secret, row["unova_dex_number"])

def write_csv(rows, filepath):
    if not rows:
        raise ValueError("No rows to write.")

    rows = sorted(rows, key=binder_sort_key)
    fieldnames = list(rows[0].keys())

    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

write_csv(data_rows, "./data/unova_cards.csv")