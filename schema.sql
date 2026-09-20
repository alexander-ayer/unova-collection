CREATE DATABASE IF NOT EXISTS unova_collection;
USE unova_collection;

CREATE TABLE cards (
    card_id INT AUTO_INCREMENT PRIMARY KEY,
    unova_dex_number INT NOT NULL,
    pokemon_name VARCHAR(50) NOT NULL,
    rarity ENUM('C', 'U', 'R', 'RR', 'RH', 'PB', 'MB', 'IR', 'UR', 'SIR', 'BWR') NOT NULL,
    card_set VARCHAR(3) NOT NULL,
    card_number VARCHAR(10) NOT NULL,
    card_type ENUM('Grass', 'Fire', 'Water', 'Lightning', 'Psychic', 'Fighting', 'Darkness', 'Metal', 'Dragon', 'Colorless') NOT NULL,
    acquired BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE KEY unique_card_variant (card_set, card_number, rarity),
    INDEX idx_dex_number (unova_dex_number)
);