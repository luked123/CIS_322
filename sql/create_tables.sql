-- create_tables.sql 
-- Creator: Luke Donnelly  
-- Assignment 7  



CREATE TABLE roles (
	role_pk		SERIAL PRIMARY KEY,               -- Decided to create a role table. Roles will be handled through 
							  -- a serial key. 
							  -- Roles should be able to be manipulated easily and having its own  
	role		varchar(32) UNIQUE             	  -- table allows that.		
);


CREATE TABLE users (
	user_pk 	SERIAL PRIMARY KEY,               -- Decided to include a numeric key.
       							  -- Usernames should just be in  the users table.	

	username 	varchar(16) UNIQUE NOT NULL,      -- Req doc states usernames cannot be longer than 16 chars.
       							  -- Usernames should be unique, cannot create an empty user.

	password 	varchar(16) NOT NULL,	          -- Req doc states passwords cannot be longer than 16 chars.

	role_fk		INTEGER REFERENCES roles (role_pk)  -- References roles table
);


CREATE TABLE facilities (
	facility_pk	SERIAL PRIMARY KEY,                             -- Facilities are associated with a primary key. 

	facility_name 	varchar(32) UNIQUE,                             -- Facility name must be unique.

	facility_code	varchar(6)  UNIQUE                              -- Facility code must be unique.
);


CREATE TABLE assets ( 
	asset_pk 	SERIAL PRIMARY KEY, 		  		-- Assets  are associated with a primary key.
	
	asset_tag	varchar(16) UNIQUE NOT NULL,			-- Asset tags must be unique.	

	asset_desc	TEXT, 						

	asset_at	INTEGER REFERENCES facilities ( facility_pk)	-- Disposed will be apart of facilities as a DISPOSED										-- name, and facility code of 0.  Will be easy to see 
);                                                                      -- all assets that have been dipsosed.  

CREATE TABLE transit (
	asset_fk 	INTEGER REFERENCES assets ( asset_pk),           -- References the asset in transit.
	
	source_fk 	INTEGER REFERENCES facilities ( facility_pk),	 -- References where the assets from.

	final_fk	INTEGER REFERENCES facilities ( facility_pk),    -- References where the asset is at.

	depart_dt	DATE,                                            -- Date it departed source.

	arrival_dt 	DATE                                             -- Date it arrived at final. 
); 

