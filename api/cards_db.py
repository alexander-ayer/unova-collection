from connection import get_connection

SELECT_CARDS = """
    SELECT card_id, unova_dex_number, pokemon_name, card_number,
           card_set, card_type, rarity, acquired
    FROM cards
"""

BINDER_ORDER = """
    ORDER BY
        CASE
            WHEN rarity = 'BWR' THEN 2
            WHEN rarity IN ('IR', 'SIR') THEN 1
            ELSE 0
        END,
        unova_dex_number,
        card_set,
        FIELD(rarity, 'C', 'U', 'R', 'RH', 'PB', 'MB', 'RR', 'UR', 'IR', 'SIR', 'BWR'),
        card_number
"""


def get_cards(
    card_set: str | None = None,
    rarity: str | None = None,
    acquired: bool | None = None,
    name: str | None = None,
) -> list[dict]:
    conditions = []
    params = []

    if card_set is not None:
        conditions.append("card_set = %s")
        params.append(card_set)
    if rarity:
        placeholders = ", ".join(["%s"] * len(rarity))
        conditions.append(f"rarity IN ({placeholders})")
        params.extend(rarity)
    if acquired is not None:
        conditions.append("acquired = %s")
        params.append(acquired)
    if name is not None:
        conditions.append("pokemon_name LIKE %s")
        params.append(f"%{name}%")

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    query = f"{SELECT_CARDS} {where} {BINDER_ORDER}"

    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        conn.close()