CREATE TABLE IF NOT EXISTS "transaction" (
    id INTEGER NOT NULL,
    date_of_movement DATETIME,
    description VARCHAR(30),
    value REAL NOT NULL,
    origin VARCHAR(5),
    PRIMARY KEY (id)
);
