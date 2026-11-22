from connection import get_connection

BINDER_ORDER_QUERY = """
    SELECT card_id, unova_dex_number, pokemon_name, card_number,
           card_set, card_type, rarity, acquired
    FROM cards
    ORDER BY
        CASE WHEN rarity IN ('IR', 'SIR', 'BWR') THEN 1 ELSE 0 END,
        unova_dex_number,
        card_set,
        FIELD(rarity, 'C', 'U', 'R', 'RH', 'PB', 'MB', 'RR', 'UR', 'IR', 'SIR', 'BWR'),
        card_number
"""

def get_all_cards() -> list[dict]:
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(BINDER_ORDER_QUERY)
        return cursor.fetchall()
    finally:
        conn.close()