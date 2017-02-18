-- create_tables.sql */
-- Creator: Luke Donnelly */ 
-- Assignment 6  



CREATE TABLE users (
	user_pk 	SERIAL PRIMARY KEY,               -- decided to include a numeric key
       							  -- usernames should just be in  the users table	

	username 	varchar(16) UNIQUE NOT NULL,      -- req doc states usernames cannot be longer than 16 chars
       							  -- usernames should be unique, cannot create an empty user

	password 	varchar(16) NOT NULL	          -- req doc states passwords cannot be longer than 16 chars
);



