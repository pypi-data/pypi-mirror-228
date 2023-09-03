
CREATE TABLE IF NOT EXISTS account (
    id INTEGER NOT NULL,
    name VARCHAR(30),
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS balance (
    id INTEGER NOT NULL,
    value REAL NOT NULL,
    account_id INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (account_id) REFERENCES account(id)
);

