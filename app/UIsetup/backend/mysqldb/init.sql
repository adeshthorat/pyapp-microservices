CREATE DATABASE IF NOT EXISTS userdb;
USE userdb;

CREATE TABLE IF NOT EXISTS users (
  id INT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  city VARCHAR(100)
);

INSERT INTO users (id) VALUES ('1');
INSERT INTO users (name) VALUES ('InitialUser');
INSERT INTO users (email) VALUES ('fakeuser@gmail.com');
INSERT INTO users (city) VALUES ('Perth');
