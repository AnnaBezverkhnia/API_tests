DROP TABLE IF EXISTS intercoms;

CREATE TABLE intercoms (
    id INTEGER NOT NULL PRIMARY KEY,
    ip TEXT NOT NULL,
    model TEXT NOT NULL,
    intercom_password TEXT NOT NULL,
    firmware TEXT NOT NULL,
    add_device TEXT,
    test_path TEXT
);