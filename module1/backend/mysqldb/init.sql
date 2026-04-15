CREATE DATABASE IF NOT EXISTS userdb;
USE userdb;

CREATE TABLE IF NOT EXISTS users (
  id INT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  city VARCHAR(100)
);

INSERT INTO users (id, name, email, city) VALUES (1, 'InitialUser', 'fakeuser@gmail.com', 'Perth');
