INSERT INTO User ('user1', 'user1@gmail.com','pass1');
INSERT INTO User ('user2', 'user1@gmail.com','pass2');
INSERT INTO User ('user3', 'user1@gmail.com','pass3');

INSERT INTO Type ('Normal');
INSERT INTO Type ('Fire');
INSERT INTO Type ('Water');
INSERT INTO Type ('Grass');
INSERT INTO Type ('Electric');
INSERT INTO Type ('Ice');
INSERT INTO Type ('Fighting');
INSERT INTO Type ('Poison');
INSERT INTO Type ('Ground');
INSERT INTO Type ('Flying');
INSERT INTO Type ('Psychic');
INSERT INTO Type ('Bug');
INSERT INTO Type ('Rock');
INSERT INTO Type ('Ghost');
INSERT INTO Type ('Dark');
INSERT INTO Type ('Dragon');
INSERT INTO Type ('Steel');
INSERT INTO Type ('Fairy');

INSERT INTO Effectiveness('Normal', 'Normal', 1);
INSERT INTO Effectiveness('Normal', 'Ghost', 0);
INSERT INTO Effectiveness('Rock', 'Fighting', 0.5);
INSERT INTO Effectiveness('Fighting', 'Normal', 2);

INSERT INTO Pokemon(1, 'Bulbasaur', 45, 45, 49, 49, 65, 65, 'Grass', 'Poison', 'Overgrow', 'Chlorophyll', NULL, FALSE, FALSE);
INSERT INTO Pokemon(2, 'Ivysaur', 60, 60, 62, 63, 80, 80, 'Grass', 'Poison', 'Overgrow', 'Chlorophyll', 1, FALSE, FALSE);
INSERT INTO Pokemon(3, 'Venusaur', 80, 80, 100, 123, 122, 120, 'Grass', 'Poison', 'Overgrow', 'Chlorophyll', 2, FALSE, FALSE);
INSERT INTO Pokemon(4, 'Charmander', 39, 65, 52, 43, 60, 50, 'Fire', NULL, 'Blaze', 'Solar Power', NULL, FALSE, FALSE);
INSERT INTO Pokemon(5, 'Charmeleon', 58, 80, 64, 58, 80, 65, 'Fire', NULL, 'Blaze', 'Solar Power', 4, FALSE, FALSE);
INSERT INTO Pokemon(6, 'Charizard', 78, 100, 104, 78, 159, 115, 'Fire', 'Flying', 'Blaze', 'Solar Power', 5, FALSE, FALSE);
INSERT INTO Pokemon(7, 'Squirtle', 44, 43, 48, 65, 50, 64, 'Water', NULL, 'Torrent', 'Rain Dish', NULL, FALSE, FALSE);
INSERT INTO Pokemon(8, 'Wartortle', 59, 58, 63, 80, 65, 80, 'Water', NULL, 'Torrent', 'Rain Dish', NULL, FALSE, FALSE);
INSERT INTO Pokemon(9, 'Blastoise', 79, 78, 103, 120, 135, 115'Water', NULL, 'Torrent', 'Rain Dish', NULL, FALSE, FALSE);

-- Note: couldn't find dataset for this, making up some for now
INSERT INTO PokemonPairings(3, 6, 0.1);
INSERT INTO PokemonPairings(3, 9, 0.2);
INSERT INTO PokemonPairings(6, 9, 0.05);

-- Using random teams because of limited pokemon
INSERT INTO Team(1, 2, 3, 4, 5, 6, 1, 10, 5);
INSERT INTO Team(2, 3, 4, 5, 6, 9, 2, 20, 10);
INSERT INTO Team(3, 5, 6, 7, 8, 9, 3, 30, 15);

INSERT INTO Move('Pound', 'Normal', 35, 40, 'physical', 100);
INSERT INTO Move('Razor Leaf', 'Grass', 25, 55, 'physical', 95);
INSERT INTO Move('Solar Beam', 'Grass', 10, 120, 'special', 100);
INSERT INTO Move('Bubble', 'Water', 30, 40, 'special', 100);
INSERT INTO Move('Ember', 'Fire', 25, 40, 'special', 100);

INSERT INTO CanLearnMove(1, 'Razor Leaf');
INSERT INTO CanLearnMove(2, 'Razor Leaf');
INSERT INTO CanLearnMove(3, 'Razor Leaf');
INSERT INTO CanLearnMove(3, 'Solar Beam');
INSERT INTO CanLearnMove(4, 'Ember');
INSERT INTO CanLearnMove(7, 'Bubble');

INSERT INTO OwnedPokemon(1, 'user1', 'Bulby', 2, 'male', FALSE, 10, 10, 10, 10, 10, 10, 'Overgrow', 'Razor Leaf', NULL, NULL, NULL);
INSERT INTO OwnedPokemon(4, 'user2', 'Char', 2, 'female', FALSE, 11, 11, 11, 11, 11, 11, 'Blaze', 'Ember', NULL, NULL, NULL);
INSERT INTO OwnedPokemon(7, 'user3', 'Turtle', 2, 'male', FALSE, 12, 12, 12, 12, 12, 12, 'Torrent', 'Bubble', NULL, NULL, NULL);