CREATE DATABASE IF NOT EXISTS users;
USE users;

CREATE TABLE IF NOT EXISTS users (
    uid INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(80) UNIQUE NOT NULL,
    age INTEGER NOT NULL
);

INSERT INTO users (name, age) VALUES ('John', 30), ('Jane', 25);