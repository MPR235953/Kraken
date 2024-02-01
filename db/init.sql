CREATE DATABASE IF NOT EXISTS currencies;
USE currencies;

CREATE TABLE eur_pln (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `Date` DATE,
    `Open` DOUBLE,
    `High` DOUBLE,
    `Low` DOUBLE,
    `Close` DOUBLE,
    `Adj Close` DOUBLE,
    `Volume` BIGINT
);

CREATE TABLE pln_eur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `Date` DATE,
    `Open` DOUBLE,
    `High` DOUBLE,
    `Low` DOUBLE,
    `Close` DOUBLE,
    `Adj Close` DOUBLE,
    `Volume` BIGINT
);

CREATE TABLE usd_pln (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `Date` DATE,
    `Open` DOUBLE,
    `High` DOUBLE,
    `Low` DOUBLE,
    `Close` DOUBLE,
    `Adj Close` DOUBLE,
    `Volume` BIGINT
);

CREATE TABLE pln_usd (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `Date` DATE,
    `Open` DOUBLE,
    `High` DOUBLE,
    `Low` DOUBLE,
    `Close` DOUBLE,
    `Adj Close` DOUBLE,
    `Volume` BIGINT
);

CREATE TABLE eur_usd (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `Date` DATE,
    `Open` DOUBLE,
    `High` DOUBLE,
    `Low` DOUBLE,
    `Close` DOUBLE,
    `Adj Close` DOUBLE,
    `Volume` BIGINT
);

CREATE TABLE usd_eur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `Date` DATE,
    `Open` DOUBLE,
    `High` DOUBLE,
    `Low` DOUBLE,
    `Close` DOUBLE,
    `Adj Close` DOUBLE,
    `Volume` BIGINT
);