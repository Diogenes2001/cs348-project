-- FEATURE 1

-- Example without move querying

SELECT id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2
FROM Pokemon
WHERE name LIKE '%Char%' AND baseHp >= 30 
AND (ability1 LIKE '%Blaze%' OR ability2 LIKE '%Blaze%');

-- Example with move querying

SELECT id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2, STRING_AGG(Move.moveName, ', ' ORDER BY Move.moveName) FROM (
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
(type1 = 'Ground' OR type2 = 'Ground') AND Move.moveName = 'Draco Meteor'
GROUP BY id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2;

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
	WHERE evolvesFrom = 280
);

----------------------------------------------------
-- FEATURE 3: User signup / login with authentication and encrypted passwords

-- Example signup / adding new users
INSERT INTO "User"(username, email, "password")
VALUES('username', 'email@address', 'encrypted_password');

-- Example login with authentication / verifying old password
SELECT "password"
FROM "User"
WHERE username = 'username';

-- Example changing password

UPDATE "User"
SET "password" = 'new_encrypted_password'
WHERE username = 'username';

-- Example deleting user
DELETE FROM "User"
WHERE username = 'username';

----------------------------------------------------
-- FEATURE 4: User-owned pokemon

-- Example insertion

INSERT INTO OwnedPokemon (species, owner, nickname, level, ability, move1)
	SELECT id, 'user1', 'Dragon', 5, 'Blaze', 'Ember' FROM Pokemon
	WHERE name = 'Charmander';

-- Check the inserted tuple

SELECT * FROM OwnedPokemon WHERE ownedID=56;

-- Example modification

UPDATE OwnedPokemon SET species = (SELECT id FROM Pokemon WHERE name='Charmander'), 
	level = 3, hp = 15, def = 20
WHERE ownedID = 56;

-- Check the inserted tuple

SELECT * FROM OwnedPokemon WHERE ownedID=56;

-- Example deletion

DELETE FROM OwnedPokemon WHERE ownedID = 56;

-- Check the tuple no longer exists

SELECT * FROM OwnedPokemon WHERE ownedID=56;

----------------------------------------------------
-- FEATURE 5: Recommending Program-Generated Pokemon Teams

SELECT
    Pokemon1.id as pid1,
    Pokemon2.id as pid2,
    Pokemon3.id as pid3,
    Pokemon4.id as pid4,
    Pokemon5.id as pid5,
    Pokemon6.id as pid6
FROM Pokemon as Pokemon1
    INNER JOIN Pokemon as Pokemon2
	    ON  Pokemon1.id < Pokemon2.id
	    AND Pokemon1.type1 <> Pokemon2.type1
    INNER JOIN Pokemon as Pokemon3
	    ON 	Pokemon2.id < Pokemon3.id
	    AND Pokemon1.type1 <> Pokemon3.type1
	    AND Pokemon2.type1 <> Pokemon3.type1
    INNER JOIN Pokemon as Pokemon4
	    ON 	Pokemon3.id < Pokemon4.id
	    AND Pokemon1.type1 <> Pokemon4.type1
	    AND Pokemon2.type1 <> Pokemon4.type1
	    AND Pokemon3.type1 <> Pokemon4.type1
    INNER JOIN Pokemon as Pokemon5
	    ON  Pokemon4.id < Pokemon5.id
	    AND Pokemon1.type1 <> Pokemon5.type1
	    AND Pokemon2.type1 <> Pokemon5.type1
	    AND Pokemon3.type1 <> Pokemon5.type1
	    AND Pokemon4.type1 <> Pokemon5.type1
    INNER JOIN Pokemon as Pokemon6
        ON 	Pokemon5.id < Pokemon6.id
        AND Pokemon1.type1 <> Pokemon6.type1
        AND Pokemon2.type1 <> Pokemon6.type1
        AND Pokemon3.type1 <> Pokemon6.type1
        AND Pokemon4.type1 <> Pokemon6.type1
        AND Pokemon5.type1 <> Pokemon6.type1
    LEFT JOIN PokemonPairings as Pokemon12
        ON 	Pokemon12.pid1 = Pokemon1.id
        AND	Pokemon12.pid2 = Pokemon2.id
    LEFT JOIN PokemonPairings as Pokemon13
        ON 	Pokemon13.pid1 = Pokemon1.id
        AND	Pokemon13.pid2 = Pokemon3.id
    LEFT JOIN PokemonPairings as Pokemon14
        ON 	Pokemon14.pid1 = Pokemon1.id
        AND	Pokemon14.pid2 = Pokemon4.id
    LEFT JOIN PokemonPairings as Pokemon15
        ON 	Pokemon15.pid1 = Pokemon1.id
        AND	Pokemon15.pid2 = Pokemon5.id
    LEFT JOIN PokemonPairings as Pokemon16
        ON 	Pokemon16.pid1 = Pokemon1.id
        AND	Pokemon16.pid2 = Pokemon6.id
    LEFT JOIN PokemonPairings as Pokemon23
        ON 	Pokemon23.pid1 = Pokemon2.id
        AND	Pokemon23.pid2 = Pokemon3.id
    LEFT JOIN PokemonPairings as Pokemon24
        ON 	Pokemon24.pid1 = Pokemon2.id
        AND	Pokemon24.pid2 = Pokemon4.id
    LEFT JOIN PokemonPairings as Pokemon25
        ON 	Pokemon25.pid1 = Pokemon2.id
        AND	Pokemon25.pid2 = Pokemon5.id
    LEFT JOIN PokemonPairings as Pokemon26
        ON 	Pokemon26.pid1 = Pokemon2.id
        AND	Pokemon26.pid2 = Pokemon6.id
    LEFT JOIN PokemonPairings as Pokemon34
        ON 	Pokemon34.pid1 = Pokemon3.id
        AND	Pokemon34.pid2 = Pokemon4.id
    LEFT JOIN PokemonPairings as Pokemon35
        ON 	Pokemon35.pid1 = Pokemon3.id
        AND	Pokemon35.pid2 = Pokemon5.id
    LEFT JOIN PokemonPairings as Pokemon36
        ON 	Pokemon36.pid1 = Pokemon3.id
        AND	Pokemon36.pid2 = Pokemon6.id
    LEFT JOIN PokemonPairings as Pokemon45
        ON 	Pokemon45.pid1 = Pokemon4.id
        AND	Pokemon45.pid2 = Pokemon5.id
    LEFT JOIN PokemonPairings as Pokemon46
        ON 	Pokemon46.pid1 = Pokemon4.id
        AND	Pokemon46.pid2 = Pokemon6.id
    LEFT JOIN PokemonPairings as Pokemon56
        ON 	Pokemon56.pid1 = Pokemon5.id
        AND	Pokemon56.pid2 = Pokemon6.id
ORDER BY
    COALESCE(Pokemon12.percentage, 0) +
    COALESCE(Pokemon13.percentage, 0) +
    COALESCE(Pokemon14.percentage, 0) +
    COALESCE(Pokemon15.percentage, 0) +
    COALESCE(Pokemon16.percentage, 0) +
    COALESCE(Pokemon23.percentage, 0) +
    COALESCE(Pokemon24.percentage, 0) +
    COALESCE(Pokemon25.percentage, 0) +
    COALESCE(Pokemon26.percentage, 0) +
    COALESCE(Pokemon34.percentage, 0) +
    COALESCE(Pokemon35.percentage, 0) +
    COALESCE(Pokemon36.percentage, 0) +
    COALESCE(Pokemon45.percentage, 0) +
    COALESCE(Pokemon46.percentage, 0) +
    COALESCE(Pokemon56.percentage, 0) DESC
LIMIT 5;

----------------------------------------------------
-- FEATURE 6: Recommending User-Generated Pokemon Teams

-- Example declaring the cursor
DECLARE UserTeamsCursor CURSOR WITH HOLD FOR
SELECT *
FROM Team
ORDER BY CAST(wins AS FLOAT) / CAST(wins + losses AS FLOAT) DESC;

-- Example fetching the next Pokemon team
FETCH NEXT FROM UserTeamsCursor;
FETCH NEXT FROM UserTeamsCursor;
FETCH NEXT FROM UserTeamsCursor;
