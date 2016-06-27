-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- Player Table

CREATE TABLE players(id SERIAL primary key,
					 name TEXT
					);

-- Matches Table
CREATE TABLE matches(id SERIAL primary key,
				     winner_id INTEGER references players(id) ON DELETE CASCADE,
				     loser_id INTEGER references players(id) ON DELETE CASCADE
					);

CREATE VIEW v_matches AS(
						 SELECT id, name,
						
						(SELECT count(*) FROM matches WHERE winner_id = players.id) AS wins, 
						
						(SELECT count(*) FROM matches WHERE players.id = winner_id OR players.id = loser_id) AS matches

						 FROM players
						);