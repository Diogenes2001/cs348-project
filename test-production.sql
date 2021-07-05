-- FEATURE 1

-- Example without move querying

SELECT id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2
FROM Pokemon
WHERE name ILIKE '%char%' AND baseHp >= 30 
AND (type1 = 'Fire' OR type2 = 'Fire')
ORDER BY id;

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
(type1 = 'Ground' OR type2 = 'Ground') AND Move.moveName ILIKE '%Draco Meteor%'
GROUP BY id, name, baseHp, baseSpd, baseAtk, baseDef, baseSpAtk, baseSpDef, type1, type2
ORDER BY id;

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

-- No filters
SELECT
    p1id,
    p1name,
    p2id,
    p2name,
    p3id,
    p3name,
    p4id,
    p4name,
    p5id,
    p5name,
    Pokemon6.id as p6id,
    Pokemon6.name as p6name
FROM
    (SELECT
        p1id,
        p1name,
        p1type,
        p2id,
        p2name,
        p2type,
        p3id,
        p3name,
        p3type,
        p4id,
        p4name,
        p4type,
        Pokemon5.id as p5id,
        Pokemon5.name as p5name,
        Pokemon5.type1 as p5type
    FROM
        (SELECT
            p1id,
            p1name,
            p1type,
            p2id,
            p2name,
            p2type,
            p3id,
            p3name,
            p3type,
            Pokemon4.id as p4id,
            Pokemon4.name as p4name,
            Pokemon4.type1 as p4type
        FROM
            (SELECT
                p1id,
                p1name,
                p1type,
                p2id,
                p2name,
                p2type,
                Pokemon3.id as p3id,
                Pokemon3.name as p3name,
                Pokemon3.type1 as p3type
            FROM
                (SELECT
                    Pokemon1.id as p1id,
                    Pokemon1.name as p1name,
                    Pokemon1.type1 as p1type,
                    Pokemon2.id as p2id,
                    Pokemon2.name as p2name,
                    Pokemon2.type1 as p2type
                FROM Pokemon as Pokemon1
                INNER JOIN Pokemon as Pokemon2
                    ON Pokemon1.id <> Pokemon2.id
                    AND Pokemon1.id < Pokemon2.id
                    AND Pokemon1.type1 <> Pokemon2.type1
                LEFT JOIN PokemonPairings as Pokemon12
                    ON 	Pokemon12.pid1 = Pokemon1.id
                    AND	Pokemon12.pid2 = Pokemon2.id
                ORDER BY
                    COALESCE(Pokemon12.percentage, 0) DESC
                LIMIT 1000) as Pokemon12
            INNER JOIN Pokemon as Pokemon3
                ON  p1id <> Pokemon3.id
                AND	p2id < Pokemon3.id
                AND p1type <> Pokemon3.type1
                AND p2type <> Pokemon3.type1
            LEFT JOIN PokemonPairings as Pokemon13
                ON 	Pokemon13.pid1 = p1id
                AND	Pokemon13.pid2 = Pokemon3.id
            LEFT JOIN PokemonPairings as Pokemon23
                ON 	Pokemon23.pid1 = p2id
                AND Pokemon23.pid2 = Pokemon3.id
            ORDER BY
                COALESCE(Pokemon13.percentage, 0) +
                COALESCE(Pokemon23.percentage, 0) DESC
            LIMIT 1000) as Pokemon123
        INNER JOIN Pokemon as Pokemon4
            ON  p1id <> Pokemon4.id
            AND p3id < Pokemon4.id
            AND p1type <> Pokemon4.type1
            AND p2type <> Pokemon4.type1
            AND p3type <> Pokemon4.type1
        LEFT JOIN PokemonPairings as Pokemon14
            ON 	Pokemon14.pid1 = p1id
            AND	Pokemon14.pid2 = Pokemon4.id
        LEFT JOIN PokemonPairings as Pokemon24
            ON 	Pokemon24.pid1 = p2id
            AND	Pokemon24.pid2 = Pokemon4.id
        LEFT JOIN PokemonPairings as Pokemon34
            ON 	Pokemon34.pid1 = p3id
            AND	Pokemon34.pid2 = Pokemon4.id
        ORDER BY
            COALESCE(Pokemon14.percentage, 0) +
            COALESCE(Pokemon24.percentage, 0) +
            COALESCE(Pokemon34.percentage, 0) DESC
        LIMIT 1000) as Pokemon1234
    INNER JOIN Pokemon as Pokemon5
        ON  p1id <> Pokemon5.id
        AND p4id < Pokemon5.id
        AND p1type <> Pokemon5.type1
        AND p2type <> Pokemon5.type1
        AND p3type <> Pokemon5.type1
        AND p4type <> Pokemon5.type1
    LEFT JOIN PokemonPairings as Pokemon15
        ON 	Pokemon15.pid1 = p1id
        AND	Pokemon15.pid2 = Pokemon5.id
    LEFT JOIN PokemonPairings as Pokemon25
        ON 	Pokemon25.pid1 = p2id
        AND	Pokemon25.pid2 = Pokemon5.id
    LEFT JOIN PokemonPairings as Pokemon35
        ON 	Pokemon35.pid1 = p3id
        AND	Pokemon35.pid2 = Pokemon5.id
    LEFT JOIN PokemonPairings as Pokemon45
        ON 	Pokemon45.pid1 = p4id
        AND	Pokemon45.pid2 = Pokemon5.id
    ORDER BY
        COALESCE(Pokemon15.percentage, 0) +
        COALESCE(Pokemon25.percentage, 0) +
        COALESCE(Pokemon35.percentage, 0) +
        COALESCE(Pokemon45.percentage, 0) DESC
    LIMIT 1000) as Pokemon12345
INNER JOIN Pokemon as Pokemon6
    ON  p1id <> Pokemon6.id
    AND p5id < Pokemon6.id
    AND p1type <> Pokemon6.type1
    AND p2type <> Pokemon6.type1
    AND p3type <> Pokemon6.type1
    AND p4type <> Pokemon6.type1
    AND p5type <> Pokemon6.type1
LEFT JOIN PokemonPairings as Pokemon16
    ON 	Pokemon16.pid1 = p1id
    AND	Pokemon16.pid2 = Pokemon6.id
LEFT JOIN PokemonPairings as Pokemon26
    ON 	Pokemon26.pid1 = p2id
    AND	Pokemon26.pid2 = Pokemon6.id
LEFT JOIN PokemonPairings as Pokemon36
    ON 	Pokemon36.pid1 = p3id
    AND	Pokemon36.pid2 = Pokemon6.id
LEFT JOIN PokemonPairings as Pokemon46
    ON 	Pokemon46.pid1 = p4id
    AND	Pokemon46.pid2 = Pokemon6.id
LEFT JOIN PokemonPairings as Pokemon56
    ON 	Pokemon56.pid1 = p5id
    AND	Pokemon56.pid2 = Pokemon6.id
ORDER BY
    COALESCE(Pokemon16.percentage, 0) +
    COALESCE(Pokemon26.percentage, 0) +
    COALESCE(Pokemon36.percentage, 0) +
    COALESCE(Pokemon46.percentage, 0) +
    COALESCE(Pokemon56.percentage, 0) DESC
LIMIT 5;

-- Filter teams with Charizard
SELECT
    p1id,
    p1name,
    p2id,
    p2name,
    p3id,
    p3name,
    p4id,
    p4name,
    p5id,
    p5name,
    Pokemon6.id as p6id,
    Pokemon6.name as p6name
FROM
    (SELECT
        p1id,
        p1name,
        p1type,
        p2id,
        p2name,
        p2type,
        p3id,
        p3name,
        p3type,
        p4id,
        p4name,
        p4type,
        Pokemon5.id as p5id,
        Pokemon5.name as p5name,
        Pokemon5.type1 as p5type
    FROM
        (SELECT
            p1id,
            p1name,
            p1type,
            p2id,
            p2name,
            p2type,
            p3id,
            p3name,
            p3type,
            Pokemon4.id as p4id,
            Pokemon4.name as p4name,
            Pokemon4.type1 as p4type
        FROM
            (SELECT
                p1id,
                p1name,
                p1type,
                p2id,
                p2name,
                p2type,
                Pokemon3.id as p3id,
                Pokemon3.name as p3name,
                Pokemon3.type1 as p3type
            FROM
                (SELECT
                    Pokemon1.id as p1id,
                    Pokemon1.name as p1name,
                    Pokemon1.type1 as p1type,
                    Pokemon2.id as p2id,
                    Pokemon2.name as p2name,
                    Pokemon2.type1 as p2type
                FROM Pokemon as Pokemon1
                INNER JOIN Pokemon as Pokemon2
                    ON Pokemon1.id <> Pokemon2.id
                    AND Pokemon1.type1 <> Pokemon2.type1
                LEFT JOIN PokemonPairings as Pokemon12
                    ON 	Pokemon12.pid1 = Pokemon1.id
                    AND	Pokemon12.pid2 = Pokemon2.id
                WHERE LOWER(Pokemon1.name) = LOWER('Charizard')
                ORDER BY
                    COALESCE(Pokemon12.percentage, 0) DESC
                LIMIT 1000) as Pokemon12
            INNER JOIN Pokemon as Pokemon3
                ON  p1id <> Pokemon3.id
                AND	p2id < Pokemon3.id
                AND p1type <> Pokemon3.type1
                AND p2type <> Pokemon3.type1
            LEFT JOIN PokemonPairings as Pokemon13
                ON 	Pokemon13.pid1 = p1id
                AND	Pokemon13.pid2 = Pokemon3.id
            LEFT JOIN PokemonPairings as Pokemon23
                ON 	Pokemon23.pid1 = p2id
                AND Pokemon23.pid2 = Pokemon3.id
            ORDER BY
                COALESCE(Pokemon13.percentage, 0) +
                COALESCE(Pokemon23.percentage, 0) DESC
            LIMIT 1000) as Pokemon123
        INNER JOIN Pokemon as Pokemon4
            ON  p1id <> Pokemon4.id
            AND p3id < Pokemon4.id
            AND p1type <> Pokemon4.type1
            AND p2type <> Pokemon4.type1
            AND p3type <> Pokemon4.type1
        LEFT JOIN PokemonPairings as Pokemon14
            ON 	Pokemon14.pid1 = p1id
            AND	Pokemon14.pid2 = Pokemon4.id
        LEFT JOIN PokemonPairings as Pokemon24
            ON 	Pokemon24.pid1 = p2id
            AND	Pokemon24.pid2 = Pokemon4.id
        LEFT JOIN PokemonPairings as Pokemon34
            ON 	Pokemon34.pid1 = p3id
            AND	Pokemon34.pid2 = Pokemon4.id
        ORDER BY
            COALESCE(Pokemon14.percentage, 0) +
            COALESCE(Pokemon24.percentage, 0) +
            COALESCE(Pokemon34.percentage, 0) DESC
        LIMIT 1000) as Pokemon1234
    INNER JOIN Pokemon as Pokemon5
        ON  p1id <> Pokemon5.id
        AND p4id < Pokemon5.id
        AND p1type <> Pokemon5.type1
        AND p2type <> Pokemon5.type1
        AND p3type <> Pokemon5.type1
        AND p4type <> Pokemon5.type1
    LEFT JOIN PokemonPairings as Pokemon15
        ON 	Pokemon15.pid1 = p1id
        AND	Pokemon15.pid2 = Pokemon5.id
    LEFT JOIN PokemonPairings as Pokemon25
        ON 	Pokemon25.pid1 = p2id
        AND	Pokemon25.pid2 = Pokemon5.id
    LEFT JOIN PokemonPairings as Pokemon35
        ON 	Pokemon35.pid1 = p3id
        AND	Pokemon35.pid2 = Pokemon5.id
    LEFT JOIN PokemonPairings as Pokemon45
        ON 	Pokemon45.pid1 = p4id
        AND	Pokemon45.pid2 = Pokemon5.id
    ORDER BY
        COALESCE(Pokemon15.percentage, 0) +
        COALESCE(Pokemon25.percentage, 0) +
        COALESCE(Pokemon35.percentage, 0) +
        COALESCE(Pokemon45.percentage, 0) DESC
    LIMIT 1000) as Pokemon12345
INNER JOIN Pokemon as Pokemon6
    ON  p1id <> Pokemon6.id
    AND p5id < Pokemon6.id
    AND p1type <> Pokemon6.type1
    AND p2type <> Pokemon6.type1
    AND p3type <> Pokemon6.type1
    AND p4type <> Pokemon6.type1
    AND p5type <> Pokemon6.type1
LEFT JOIN PokemonPairings as Pokemon16
    ON 	Pokemon16.pid1 = p1id
    AND	Pokemon16.pid2 = Pokemon6.id
LEFT JOIN PokemonPairings as Pokemon26
    ON 	Pokemon26.pid1 = p2id
    AND	Pokemon26.pid2 = Pokemon6.id
LEFT JOIN PokemonPairings as Pokemon36
    ON 	Pokemon36.pid1 = p3id
    AND	Pokemon36.pid2 = Pokemon6.id
LEFT JOIN PokemonPairings as Pokemon46
    ON 	Pokemon46.pid1 = p4id
    AND	Pokemon46.pid2 = Pokemon6.id
LEFT JOIN PokemonPairings as Pokemon56
    ON 	Pokemon56.pid1 = p5id
    AND	Pokemon56.pid2 = Pokemon6.id
ORDER BY
    COALESCE(Pokemon16.percentage, 0) +
    COALESCE(Pokemon26.percentage, 0) +
    COALESCE(Pokemon36.percentage, 0) +
    COALESCE(Pokemon46.percentage, 0) +
    COALESCE(Pokemon56.percentage, 0) DESC
LIMIT 5;

----------------------------------------------------
-- FEATURE 6: Recommending User-Generated Pokemon Teams

-- No filters
SELECT pid1,
       Pokemon1.name,
       pid2,
       Pokemon2.name,
       pid3,
       Pokemon3.name,
       pid4,
       Pokemon4.name,
       pid5,
       Pokemon5.name,
       pid6,
       Pokemon6.name
FROM Team
INNER JOIN Pokemon as Pokemon1
ON pid1 = Pokemon1.id
INNER JOIN Pokemon as Pokemon2
ON pid2 = Pokemon2.id
INNER JOIN Pokemon as Pokemon3
ON pid3 = Pokemon3.id
INNER JOIN Pokemon as Pokemon4
ON pid4 = Pokemon4.id
INNER JOIN Pokemon as Pokemon5
ON pid5 = Pokemon5.id
INNER JOIN Pokemon as Pokemon6
ON pid6 = Pokemon6.id
WHERE wins + losses >= 2
ORDER BY CAST(wins AS FLOAT) / CAST(wins + losses AS FLOAT) DESC
LIMIT 5;

-- Filter teams with Charizard
SELECT pid1,
       Pokemon1.name,
       pid2,
       Pokemon2.name,
       pid3,
       Pokemon3.name,
       pid4,
       Pokemon4.name,
       pid5,
       Pokemon5.name,
       pid6,
       Pokemon6.name
FROM Team
INNER JOIN Pokemon as Pokemon1
ON pid1 = Pokemon1.id
INNER JOIN Pokemon as Pokemon2
ON pid2 = Pokemon2.id
INNER JOIN Pokemon as Pokemon3
ON pid3 = Pokemon3.id
INNER JOIN Pokemon as Pokemon4
ON pid4 = Pokemon4.id
INNER JOIN Pokemon as Pokemon5
ON pid5 = Pokemon5.id
INNER JOIN Pokemon as Pokemon6
ON pid6 = Pokemon6.id
WHERE wins + losses >= 2
AND (LOWER(Pokemon1.name) = LOWER('Charizard')
OR LOWER(Pokemon2.name) = LOWER('Charizard')
OR LOWER(Pokemon3.name) = LOWER('Charizard')
OR LOWER(Pokemon4.name) = LOWER('Charizard')
OR LOWER(Pokemon5.name) = LOWER('Charizard')
OR LOWER(Pokemon6.name) = LOWER('Charizard'))
ORDER BY CAST(wins AS FLOAT) / CAST(wins + losses AS FLOAT) DESC
LIMIT 5;
