-- creating database
DROP DATABASE IF EXISTS WorldPopulation;
CREATE DATABASE IF NOT EXISTS  WorldPopulation;
USE WorldPopulation;

-- table country
CREATE TABLE countries (
    country_id INT PRIMARY KEY AUTO_INCREMENT,
    country_name VARCHAR(100) NOT NULL UNIQUE,
    land_area BIGINT NOT NULL
);

-- country table's info
CREATE TABLE Population (
    population_id INT PRIMARY KEY AUTO_INCREMENT,
    country_id INT NOT NULL,
    world_year INT,
    global_ranking INT,
    population BIGINT,
    urban_population BIGINT,
    urban_population_percent FLOAT,
    fertility_rate FLOAT,
    FOREIGN KEY (country_id)
        REFERENCES countries (country_id)
)