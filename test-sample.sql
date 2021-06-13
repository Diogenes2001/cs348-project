-- FEATURE 1

SELECT name FROM (
	(
		Pokemon
		JOIN
		CanLearnMove
		ON id=pid
	)
	JOIN 
	Move
	ON Move.moveName = CanLearnMove.moveName
)
WHERE
power >= 90 AND moveType = 'Grass';

----------------------------------------------------
-- FEATURE 2

WITH RECURSIVE
Evolution(evolvesFrom, evolvesInto) AS (
	(
		SELECT evolvesFromId, id FROM Pokemon
	)
	UNION
	(
		SELECT e1.evolvesFrom, id
		FROM Evolution e1, Pokemon p
		WHERE e1.evolvesInto = p.evolvesFromId
	)
)
SELECT * FROM Pokemon
WHERE id IN (
	SELECT evolvesInto
	FROM Evolution
	WHERE evolvesFrom = (SELECT id FROM Pokemon WHERE name='Ralts')
);

----------------------------------------------------
-- FEATURE 3



----------------------------------------------------
-- FEATURE 4: User-owned pokemon

-- Example insertion

INSERT INTO OwnedPokemon (species, owner, nickname, level, ability, move1)
	SELECT id, 'user1', 'Dragon', 5, 'Blaze', 'Ember' FROM Pokemon
	WHERE name = 'Charmander';

-- Example modification

UPDATE OwnedPokemon SET level = 3, hp = 15, def = 20
WHERE ownedID = 2;

-- Example deletion

DELETE FROM OwnedPokemon WHERE ownedID = 3;

----------------------------------------------------
-- FEATURE 5


