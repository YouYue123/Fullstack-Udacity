-- Table definitions for the catalog project.

CREATE TABLE users(id SERIAL primary key,
				   name TEXT not null,
				   email TEXT,
				   password TEXT not null);

CREATE TABLE catalogs(id SERIAL primary key,
					  name TEXT not null);

CREATE TABLE items(id SERIAL primary key,
				   catalog_id INTEGER references catalogs(id) not null,
				   owner_id INTEGER references users(id) not null,
				   name TEXT not null,
				   content TEXT not null);


INSERT INTO catalogs (name) values('Spain');
INSERT INTO catalogs(name) values('Germany');
INSERT INTO catalogs(name) values('England');
INSERT INTO catalogs(name) values('Italy');
INSERT INTO catalogs(name) values('France');