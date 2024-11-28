CREATE DATABASE Cinephile_App;
USE Cinephile_App;
CREATE TABLE Actors (
ActorID VARCHAR(10) PRIMARY KEY,
ActorName VARCHAR(50)
);
CREATE TABLE Directors (
DirectorID VARCHAR(10) PRIMARY KEY,
DirectorName VARCHAR(50)
);
CREATE TABLE Genres (
GenreID VARCHAR(10) PRIMARY KEY,
GenreName VARCHAR(50)
);
CREATE TABLE Users (
Username VARCHAR(50) PRIMARY KEY,
FirstName VARCHAR(50),
LastName VARCHAR(50),
Password VARCHAR(50) NOT NULL
);
CREATE TABLE Movies (
MovieID INT PRIMARY KEY,
MovieName VARCHAR(100),
MovieDate DATE,
MoviePlot VARCHAR(2000),
MoviePhoto VARCHAR(255),
MovieRating FLOAT
);
CREATE TABLE Movie_Actor (
MovieID INT,
ActorID VARCHAR(10),
PRIMARY KEY(MovieID, ActorID),
FOREIGN KEY(MovieID) REFERENCES Movies (MovieID) ON DELETE CASCADE,
FOREIGN KEY(ActorID) REFERENCES Actors (ActorID) ON DELETE CASCADE
);
CREATE TABLE Movie_Director (
MovieID INT,
DirectorID VARCHAR(10),
PRIMARY KEY(MovieID, DirectorID),
FOREIGN KEY(MovieID) REFERENCES Movies (MovieID) ON DELETE CASCADE,
FOREIGN KEY(DirectorID) REFERENCES Directors (DirectorID) ON DELETE CASCADE
);
CREATE TABLE Movie_Genre (
MovieID INT,
GenreID VARCHAR(10),
PRIMARY KEY(MovieID, GenreID),
FOREIGN KEY(MovieID) REFERENCES Movies (MovieID) ON DELETE CASCADE,
FOREIGN KEY(GenreID) REFERENCES Genres (GenreID) ON DELETE CASCADE
);
CREATE TABLE User_Movie (
MovieID INT,
Username VARCHAR(50),
PRIMARY KEY(MovieID, Username),
FOREIGN KEY(MovieID) REFERENCES Movies (MovieID) ON DELETE CASCADE,
FOREIGN KEY(Username) REFERENCES Users (Username) ON DELETE CASCADE
);

INSERT INTO Genres(GenreID, GenreName) 
VALUES('ACT', 'Action'), ('ADV', 'Adventure'), ('ANM', 'Anime'),
('BIO', 'Biography'), ('COM', 'Comedy'), ('CRM', 'Crime'),
('DOC', 'Documentary'), ('DRM', 'Drama'), ('FAM', 'Family'), 
('FSY', 'Fantasy'), ('FMN', 'Film-Noir'), ('GSH', 'Game-Show'),
('HST', 'History'), ('HOR', 'Horror'), ('MUS', 'Music'),
('MUL', 'Musical'), ('MYS', 'Mystery'), ('NWS', 'News'),
('RTV', 'Reality-TV'), ('ROM', 'Romance'), ('SFI', 'Sci-Fi'),
('SHT', 'Short'), ('SPT', 'Sport'), ('TLK', 'Talk-Show'),
('THR', 'Thriller'), ('WAR', 'War'), ('WST', 'Western');