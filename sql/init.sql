CREATE DATABASE IF NOT EXISTS pixelarchives;
USE pixelarchives;

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    uuid CHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des jeux
CREATE TABLE IF NOT EXISTS games (
    id CHAR(36) NOT NULL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    console VARCHAR(100) NOT NULL,
    year INT,
    genre VARCHAR(100),
    cover VARCHAR(255)
);

-- Table associative entre users et games
CREATE TABLE IF NOT EXISTS users_games (
    user_uuid CHAR(36) NOT NULL,
    game_id CHAR(36) NOT NULL,
    added_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_uuid, game_id),
    FOREIGN KEY (user_uuid) REFERENCES users(uuid) ON DELETE CASCADE,
    FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE
);

-- Insertion des jeux
INSERT INTO games (id, title, console, year, genre, cover) VALUES
('09891c4e-5b3e-11f0-8949-5527c35e8ba0', 'ActRaiser', 'Super Nintendo', 1993, 'Gestion, Plates-Formes', 'ActRaiser.jpg'),
('0f75af58-5b3c-11f0-8949-5527c35e8ba0', 'Street Fighter II: The World Warrior', 'Arcade, Super Nintendo, Gameboy', 1991, 'Combat', 'SFII.jpg'),
('1e86c930-5b39-11f0-8949-5527c35e8ba0', 'Super Mario Bros', 'NES, Gameboy Color, Gameboy Advance, Wii, Nintendo 3DS', 1985, 'Plates-Formes', 'SuperMario.jpg'),
('2869edd2-5b3e-11f0-8949-5527c35e8ba0', 'Guardian Heroes', 'Sega Saturn', 1996, 'Beat them all', 'GuardianHeroes.jpg'),
('2b5b1308-5b3d-11f0-8949-5527c35e8ba0', 'Nights into Dreams', 'Sega Saturn, Playstation 2', 1996, 'Action', 'Nights.jpg'),
('2be75793-5b3f-11f0-8949-5527c35e8ba0', 'Power Stone', 'Arcade, Dreamcast, Playstation Portable', 1999, 'Combat', 'PowerStone.jpg'),
('36ffc198-5b06-11f0-8949-5527c35e8ba0', 'Metal Slug X', 'Neo Geo', 1999, 'Run and Gun', 'MetalSlug.jpg'),
('37001c72-5b06-11f0-8949-5527c35e8ba0', 'OutRun', 'Arcade', 1986, 'Course', 'Outrun.jpg'),
('37002256-5b06-11f0-8949-5527c35e8ba0', 'Shenmue', 'Dreamcast', 1999, 'Action-Aventure', 'Shenmue.jpg'),
('3700230e-5b06-11f0-8949-5527c35e8ba0', 'Donkey Kong Country', 'Super Nintendo', 1994, 'Plates-Formes', 'DKC.jpg'),
('405cacb7-5b3a-11f0-8949-5527c35e8ba0', 'Castlevania', 'NES, Amiga, Gameboy Advance', 1986, 'Action, Plates-Formes', 'Castlevania.jpg'),
('502e1776-5b3f-11f0-8949-5527c35e8ba0', 'Panzer Dragoon', 'Sega Saturn', 1995, 'Rail Shooter', 'PanzerDragoon.jpg'),
('549deaed-5b3b-11f0-8949-5527c35e8ba0', 'Crash Bandicoot', 'Playstation 1', 1996, 'Plates-Formes', 'CrashBandicoot.jpg'),
('58961159-5b3a-11f0-8949-5527c35e8ba0', 'Final Fantasy 7', 'Playstation 1', 1997, 'RPG', 'FF7.jpg'),
('593e1e95-5b3d-11f0-8949-5527c35e8ba0', 'Kid Icarus', 'NES, Wii, Gameboy Advance', 1986, 'Plates-Formes', 'KidIcarus.jpg'),
('82a05fe6-5b3d-11f0-8949-5527c35e8ba0', 'Battletoads', 'Arcade, NES, Megadrive, Amiga, Game Gear, Gameboy, Wii', 1991, 'Action, Beat them all', 'BattleToads.jpg'),
('88443b4b-5b3e-11f0-8949-5527c35e8ba0', 'Double Dragon', 'Arcade, NES, Master System, Megadrive, Nintendo 3DS, Gameboy, Gameboy Advance, Game Gear', 1987, 'Beat them all', 'DoubleDragon.jpg'),
('9bdb5d7a-5b3b-11f0-8949-5527c35e8ba0', 'Jak and Daxter: The Precursor Legacy', 'Playstation 2', 2001, 'Aventure, Plates-Formes', 'JakandDaxter.jpg'),
('b50fe10e-5b3b-11f0-8949-5527c35e8ba0', 'Yakuza', 'Playstation 2', 2005, 'Action-Aventure, RPG', 'RGG.jpg'),
('b95e5fc3-5b3e-11f0-8949-5527c35e8ba0', 'Megaman', 'NES, Megadrive, Playstation 1, Wii, Nintendo 3DS, Xbox, Gamecube, Playstation 2', 1987, 'Action, Plates-Formes', 'MegaMan.jpg'),
('dbcd7a21-5b3b-11f0-8949-5527c35e8ba0', 'Tintin au Tibet', 'Super Nintendo, Megadrive, Game Gear, Gameboy', 1995, 'Plates-Formes, Aventure', 'Tintin.jpg'),
('f29d3422-5b38-11f0-8949-5527c35e8ba0', 'Streets of Rage 2', 'Megadrive, Game Gear, Nintendo 3DS', 1992, 'Beat them all', 'SoRII.jpg'),
('146a89fb-63b3-11f0-99ca-00155dcb47ab', 'Fate/Extra', 'Playstation Portable', 2010, 'RPG, Visual Novel, Dungeon Crawler', 'FateExtra.jpg'),
('48c6fcfd-63b3-11f0-99ca-00155dcb47ab', 'Fate/unlimited codes', 'Playstation 2, Playstation Portable', 2008, 'Combat', 'FateCode.jpg');
