-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Player Table

CREATE TABLE players(id SERIAL primary key,
					 name TEXT,
					 wins INTEGER DEFAULT 0,
					 matches INTEGER DEFAULT 0
					);

-- Matches Table
CREATE TABLE matches(id SERIAL primary key,
				     winner_id INTEGER references players(id),
				     loser_id INTEGER references players(id)
					);