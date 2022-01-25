DROP TABLE IF EXISTS tagRelations;
DROP TABLE IF EXISTS userArt;
DROP TABLE IF EXISTS artworks;
DROP TABLE IF EXISTS artists;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS users;

CREATE TABLE artists(
    id SERIAL PRIMARY KEY,
    artistName VARCHAR(250) NOT NULl,
    artistDisplayBio TEXT,
    gender VARCHAR(50)
);

CREATE TABLE tags(
    id SERIAL PRIMARY KEY,
    tag VARCHAR(150) NOT NULL
);

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) NOT NULL
);

CREATE TABLE artworks(
  id INTEGER PRIMARY KEY,
  isHighlight BOOLEAN,
  primaryImage TEXT NOT NULL,
  primaryImageSmall TEXT NOT NULL,
  department VARCHAR(150),
  objectName VARCHAR(100),
  title TEXT,
  culture VARCHAR(150),
  period VARCHAR(150),
  dynasty VARCHAR(150),
  artistPrefix VARCHAR(100),
  artistid INTEGER,
  objectDate VARCHAR(75),
  medium VARCHAR(150),
  country VARCHAR(150),
  classification VARCHAR(150),
  linkResource TEXT,
  featured BOOLEAN DEFAULT false,
  FOREIGN KEY (artistid) REFERENCES artists(id)
);

CREATE TABLE tagRelations(
  tagid INTEGER NOT NULL,
  artid INTEGER NOT NULL,
  PRIMARY KEY (tagid, artid)
);

CREATE TABLE userArt(
    userid INTEGER NOT NULL,
    artid INTEGER NOT NULL,
    isFavourite BOOLEAN DEFAULT false,
    PRIMARY KEY (userid, artid)
);

