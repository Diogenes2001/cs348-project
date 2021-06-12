CREATE TABLE "User"(
    username VARCHAR(30) NOT NULL PRIMARY KEY,
    email VARCHAR(50) NOT NULL,
    "password" VARCHAR(20) NOT NULL
);

CREATE TABLE "Type"(
    typeName VARCHAR(16) NOT NULL PRIMARY KEY,
    "image" BYTEA
);

CREATE TABLE Effectiveness(
    moveType VARCHAR(16) NOT NULL REFERENCES "Type"(typeName),
    pokemonType VARCHAR(16) NOT NULL REFERENCES "Type"(typeName),
    effectiveness DECIMAL(1,1) NOT NULL CHECK(effectiveness IN (0, 0.5, 1, 2)),
    PRIMARY KEY(moveType, pokemonType)
);

CREATE TABLE Pokemon(
    id INTEGER NOT NULL PRIMARY KEY,
    "name" VARCHAR(30) NOT NULL UNIQUE,
    baseHp INTEGER NOT NULL CHECK(baseHp >= 0),
    baseSpd INTEGER NOT NULL CHECK(baseSpd >= 0),
    baseAtk INTEGER NOT NULL CHECK(baseAtk >= 0),
    baseDef INTEGER NOT NULL CHECK(baseDef >= 0),
    baseSpAtk INTEGER NOT NULL CHECK(baseSpAtk >= 0),
    baseSpDef INTEGER NOT NULL CHECK(baseSpDef >= 0),
    type1 VARCHAR(16) NOT NULL REFERENCES "Type"(typeName),
    type2 VARCHAR(16) REFERENCES "Type"(typeName),
    ability1 VARCHAR(30) NOT NULL,
    ability2 VARCHAR(30),
    evolvesFromId INTEGER REFERENCES Pokemon(id),
    isLegendary BOOLEAN NOT NULL,
    isMythical BOOLEAN NOT NULL,
    "image" BYTEA
);

CREATE TABLE PokemonPairings(
    pid1 INTEGER NOT NULL REFERENCES Pokemon(id),
    pid2 INTEGER NOT NULL REFERENCES Pokemon(id),
    occurances INTEGER NOT NULL CHECK(occurances >= 0),
    PRIMARY KEY (pid1, pid2)
);

-- Need to check here that the pids are unique and in ascending order
CREATE TABLE Team(
    teamID SERIAL PRIMARY KEY,
    pid1 INTEGER NOT NULL REFERENCES Pokemon(id),
    pid2 INTEGER NOT NULL REFERENCES Pokemon(id),
    pid3 INTEGER NOT NULL REFERENCES Pokemon(id),
    pid4 INTEGER NOT NULL REFERENCES Pokemon(id),
    pid5 INTEGER NOT NULL REFERENCES Pokemon(id),
    pid6 INTEGER NOT NULL REFERENCES Pokemon(id),
    starter INTEGER NOT NULL CHECK(starter >= 1 AND starter <= 6),
    wins INTEGER NOT NULL CHECK(wins >= 0),
    losses INTEGER NOT NULL CHECK(losses >= 0),
    CHECK(pid1 < pid2 AND pid2 < pid3 AND pid3 < pid4 AND
        pid4 < pid5 AND pid5 < pid6)
);

CREATE TABLE Move(
    moveName VARCHAR(30) NOT NULL PRIMARY KEY,
    moveType VARCHAR(16) NOT NULL REFERENCES "Type"(typeName),
    pp INTEGER NOT NULL CHECK(pp > 0),
    power INTEGER NOT NULL 
        CHECK(power % 5 = 0 AND power >= 0 AND power <= 250),
    damageType VARCHAR(10) NOT NULL 
        CHECK(damageType IN ('physical', 'special')),
    damage INTEGER CHECK(damage >= 0),
    accuracy INTEGER 
        CHECK(accuracy % 5 = 0 AND accuracy >= 0 AND accuracy <= 100)
);

CREATE TABLE CanLearnMove(
    pid INTEGER NOT NULL REFERENCES Pokemon(id),
    moveName VARCHAR(30) NOT NULL REFERENCES Move(moveName),
    PRIMARY KEY(pid, moveName)
);

-- create trigger for ability matches
-- check that the foreign keys to canlearnmove work as expected
-- create trigger for the stat values
CREATE TABLE OwnedPokemon(
    ownedID SERIAL PRIMARY KEY,
    species INTEGER NOT NULL REFERENCES Pokemon(id),
    "owner" VARCHAR(30) NOT NULL REFERENCES "User"(username),
    nickname VARCHAR(30) NOT NULL DEFAULT 'My Pokemon',
    "level" INTEGER NOT NULL DEFAULT 1 CHECK("level" >= 1 AND "level" <= 100),
    gender VARCHAR(10) NOT NULL DEFAULT 'unknown' 
        CHECK(gender IN ('female', 'male', 'unknown')),
    isShiny BOOLEAN NOT NULL DEFAULT 'false',
    hp INTEGER NOT NULL CHECK(hp >= 0),
    atk INTEGER NOT NULL CHECK(atk >= 0),
    def INTEGER NOT NULL CHECK(def >= 0),
    spAtk INTEGER NOT NULL CHECK(spAtk >= 0),
    spDef INTEGER NOT NULL CHECK(spDef >= 0),
    spd INTEGER NOT NULL CHECK(spd >= 0),
    ability VARCHAR(30) NOT NULL,
    move1 VARCHAR(30) NOT NULL REFERENCES Move(moveName),
    move2 VARCHAR(30) REFERENCES Move(moveName),
    move3 VARCHAR(30) REFERENCES Move(moveName),
    move4 VARCHAR(30) REFERENCES Move(moveName),
    FOREIGN KEY(species, move1) REFERENCES CanLearnMove(pid, moveName),
    FOREIGN KEY(species, move2) REFERENCES CanLearnMove(pid, moveName),
    FOREIGN KEY(species, move3) REFERENCES CanLearnMove(pid, moveName),
    FOREIGN KEY(species, move4) REFERENCES CanLearnMove(pid, moveName)
);

CREATE OR REPLACE FUNCTION check_ability() RETURNS TRIGGER AS $$
BEGIN
    IF (EXISTS 
        (SELECT * FROM OwnedPokemon, Pokemon
        WHERE species = id AND ability <> ability1 AND ability <> ability2
        )) THEN
        RETURN NULL;
    ELSE
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER ValidAbility
AFTER INSERT OR UPDATE ON OwnedPokemon
EXECUTE PROCEDURE check_ability();

CREATE OR REPLACE FUNCTION fill_stats() RETURNS TRIGGER AS $$
DECLARE
    baseHp INTEGER;
    baseAtk INTEGER;
    baseDef INTEGER;
    baseSpAtk INTEGER;
    baseSpDef INTEGER;
    baseSpd INTEGER;
BEGIN

    SELECT baseHp, baseAtk, baseDef, baseSpAtk, baseSpDef, baseSpd
    INTO baseHp, baseAtk, baseDef, baseSpAtk, baseSpDef, baseSpd
        FROM Pokemon
        WHERE id = NEW.id;

    IF NEW.hp IS NULL THEN
        NEW.hp = baseHp;
    END IF;

    IF NEW.atk IS NULL THEN
        NEW.atk = baseAtk;
    END IF;

    IF NEW.def IS NULL THEN
        NEW.def = baseDef;
    END IF;

    IF NEW.spAtk IS NULL THEN
        NEW.spAtk = baseSpAtk;
    END IF;

    IF NEW.spDef IS NULL THEN
        NEW.spDef = baseSpDef;
    END IF;

    IF NEW.spd IS NULL THEN
        NEW.spd = baseSpd;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER DefaultStats
BEFORE INSERT ON OwnedPokemon
FOR EACH ROW
EXECUTE PROCEDURE fill_stats();