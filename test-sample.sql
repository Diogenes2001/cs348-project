-- FEATURE 1



----------------------------------------------------
-- FEATURE 2



----------------------------------------------------
-- FEATURE 3



----------------------------------------------------
-- FEATURE 4: User-owned pokemon

-- Example insertion

INSERT INTO OwnedPokemon (species, owner, nickname, level, ability, move1) VALUES
	(SELECT id, 'user1', 'Dragon', 5, 'Blaze', 'Ember' FROM Pokemon
	WHERE name = 'Charmander');

-- Example modification

UPDATE OwnedPokemon SET level = 3, hp = 15, def = 20
WHERE ownedID = 2;

-- Example deletion

DELETE FROM OwnedPokemon WHERE ownedID = 3;

----------------------------------------------------
-- FEATURE 5


