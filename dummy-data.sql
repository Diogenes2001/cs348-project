﻿INSERT INTO "User" VALUES ('user1', 'user1@gmail.com','pass1');
INSERT INTO "User" VALUES ('user2', 'user1@gmail.com','pass2');
INSERT INTO "User" VALUES ('user3', 'user1@gmail.com','pass3');

INSERT INTO "Type" VALUES ('Normal');
INSERT INTO "Type" VALUES ('Fire');
INSERT INTO "Type" VALUES ('Water');
INSERT INTO "Type" VALUES ('Grass');
INSERT INTO "Type" VALUES ('Electric');
INSERT INTO "Type" VALUES ('Ice');
INSERT INTO "Type" VALUES ('Fighting');
INSERT INTO "Type" VALUES ('Poison');
INSERT INTO "Type" VALUES ('Ground');
INSERT INTO "Type" VALUES ('Flying');
INSERT INTO "Type" VALUES ('Psychic');
INSERT INTO "Type" VALUES ('Bug');
INSERT INTO "Type" VALUES ('Rock');
INSERT INTO "Type" VALUES ('Ghost');
INSERT INTO "Type" VALUES ('Dark');
INSERT INTO "Type" VALUES ('Dragon');
INSERT INTO "Type" VALUES ('Steel');
INSERT INTO "Type" VALUES ('Fairy');

INSERT INTO Effectiveness VALUES ('Normal', 'Normal', 1);
INSERT INTO Effectiveness VALUES ('Normal', 'Ghost', 0);
INSERT INTO Effectiveness VALUES ('Rock', 'Fighting', 0.5);
INSERT INTO Effectiveness VALUES ('Fighting', 'Normal', 2);

INSERT INTO Pokemon VALUES (1, 'Bulbasaur', 45, 45, 49, 49, 65, 65, 'Grass', 'Poison', 'Overgrow', NULL, NULL, FALSE, FALSE);
INSERT INTO Pokemon VALUES (2, 'Ivysaur', 60, 60, 62, 63, 80, 80, 'Grass', 'Poison', 'Overgrow', NULL, 1, FALSE, FALSE);
INSERT INTO Pokemon VALUES (3, 'Venusaur', 80, 80, 100, 123, 122, 120, 'Grass', 'Poison', 'Overgrow', NULL, 2, FALSE, FALSE);
INSERT INTO Pokemon VALUES (4, 'Charmander', 39, 65, 52, 43, 60, 50, 'Fire', NULL, 'Blaze', NULL, NULL, FALSE, FALSE);
INSERT INTO Pokemon VALUES (5, 'Charmeleon', 58, 80, 64, 58, 80, 65, 'Fire', NULL, 'Blaze', NULL, 4, FALSE, FALSE);
INSERT INTO Pokemon VALUES (6, 'Charizard', 78, 100, 104, 78, 159, 115, 'Fire', 'Flying', 'Blaze', NULL, 5, FALSE, FALSE);
INSERT INTO Pokemon VALUES (7, 'Squirtle', 44, 43, 48, 65, 50, 64, 'Water', NULL, 'Torrent', NULL, NULL, FALSE, FALSE);
INSERT INTO Pokemon VALUES (8, 'Wartortle', 59, 58, 63, 80, 65, 80, 'Water', NULL, 'Torrent', NULL, 7, FALSE, FALSE);
INSERT INTO Pokemon VALUES (9, 'Blastoise', 79, 78, 103, 120, 135, 115, 'Water', NULL, 'Torrent', NULL, 8, FALSE, FALSE);
INSERT INTO Pokemon VALUES (280, 'Ralts', 28, 40, 25, 25, 45, 35, 'Psychic', 'Fairy', 'Synchronize', 'Trace', NULL, FALSE, FALSE);
INSERT INTO Pokemon VALUES (281, 'Kirlia', 38, 50, 35, 35, 65, 55, 'Psychic', 'Fairy', 'Synchronize', 'Trace', 280, FALSE, FALSE);
INSERT INTO Pokemon VALUES (282, 'Gardevoir', 68, 80, 65, 65, 125, 115, 'Fairy', 'Psychic', 'Synchronize', 'Trace', 281, FALSE, FALSE);
INSERT INTO Pokemon VALUES (475, 'Gallade', 68, 80, 125, 65, 65, 115, 'Fighting', 'Psychic', 'Steadfast', NULL, 281, FALSE, FALSE);

-- Note: couldn't find dataset for this, making up some for now
INSERT INTO PokemonPairings VALUES (3, 6, 0.1);
INSERT INTO PokemonPairings VALUES (3, 9, 0.2);
INSERT INTO PokemonPairings VALUES (6, 9, 0.05);

-- Using random teams because of limited pokemon
INSERT INTO Team VALUES (DEFAULT, 1, 2, 3, 4, 5, 6, 1, 1, 1);
INSERT INTO Team VALUES (DEFAULT, 2, 3, 4, 5, 6, 9, 2, 6, 2);
INSERT INTO Team VALUES (DEFAULT, 3, 5, 6, 7, 8, 9, 3, 10, 5);

INSERT INTO Move VALUES ('Pound', 'Normal', 35, 40, 'physical', 100);
INSERT INTO Move VALUES ('Razor Leaf', 'Grass', 25, 55, 'physical', 95);
INSERT INTO Move VALUES ('Solar Beam', 'Grass', 10, 120, 'special', 100);
INSERT INTO Move VALUES ('Bubble', 'Water', 30, 40, 'special', 100);
INSERT INTO Move VALUES ('Hydro Pump', 'Water', 5, 110, 'special', 80);
INSERT INTO Move VALUES ('Ember', 'Fire', 25, 40, 'special', 100);
INSERT INTO Move VALUES ('Fire Blast', 'Fire', 5, 110, 'special', 85);

INSERT INTO CanLearnMove VALUES (1, 'Razor Leaf');
INSERT INTO CanLearnMove VALUES (2, 'Razor Leaf');
INSERT INTO CanLearnMove VALUES (2, 'Solar Beam');
INSERT INTO CanLearnMove VALUES (3, 'Razor Leaf');
INSERT INTO CanLearnMove VALUES (3, 'Solar Beam');
INSERT INTO CanLearnMove VALUES (4, 'Ember');
INSERT INTO CanLearnMove VALUES (6, 'Ember');
INSERT INTO CanLearnMove VALUES (6, 'Solar Beam');
INSERT INTO CanLearnMove VALUES (6, 'Fire Blast');
INSERT INTO CanLearnMove VALUES (7, 'Bubble');
INSERT INTO CanLearnMove VALUES (8, 'Bubble');
INSERT INTO CanLearnMove VALUES (9, 'Bubble');
INSERT INTO CanLearnMove VALUES (9, 'Hydro Pump');

INSERT INTO OwnedPokemon VALUES (DEFAULT, 1, 'user1', 'Bulby', 2, 'male', FALSE, 10, 10, 10, 10, 10, 10, 'Overgrow', 'Razor Leaf', NULL, NULL, NULL);
INSERT INTO OwnedPokemon VALUES (DEFAULT, 4, 'user2', 'Char', 2, 'female', FALSE, 11, 11, 11, 11, 11, 11, 'Blaze', 'Ember', NULL, NULL, NULL);
INSERT INTO OwnedPokemon VALUES (DEFAULT, 7, 'user3', 'Turtle', 2, 'male', FALSE, 12, 12, 12, 12, 12, 12, 'Torrent', 'Bubble', NULL, NULL, NULL);
