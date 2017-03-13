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

	role_fk		INTEGER REFERENCES roles (role_pk),  -- References roles table

	active		BOOLEAN				     -- user is active or not	
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

	asset_at	INTEGER REFERENCES facilities ( facility_pk)	-- Disposed will be apart of facilities as a DISPOSED										-- name, and facility code of NULL. Will be easy to see 
);                                                                      -- all assets that have been dipsosed. May change this 
									-- later. 

CREATE TABLE transit (
	asset_fk 	INTEGER REFERENCES assets ( asset_pk),           -- References the asset in transit.
	
	source_fk 	INTEGER REFERENCES facilities ( facility_pk),	 -- References where the assets from.

	final_fk	INTEGER REFERENCES facilities ( facility_pk),    -- References where the asset is at.

	depart_dt	DATE,                                            -- Date it departed source.

	arrival_dt 	DATE,                                            -- Date it arrived at final. 

	dispose_dt 	DATE                                             -- Date asset was dispossed if applicable
); 


CREATE TABLE transfer_req (
	transfer_pk 	SERIAL PRIMARY KEY,				 -- Transfer request should be differentiated.

	log_fk 		INTEGER REFERENCES users ( user_pk),             -- Logistic officer making the request.

	asset_fk	INTEGER REFERENCES assets ( asset_pk),		 -- Asset to be transfered. 

	source_fk  	INTEGER REFERENCES facilities ( facility_pk),    -- Where the asset is located currently.

	dest_fk		INTEGER REFERENCES facilities ( facility_pk),    -- Where the asset is requested to go.

	req_dt		TIMESTAMP, 						 -- Date request was made. 

	fac_fk		INTEGER REFERENCES users ( user_pk),             -- Facilities officer that approve/ deny request.   

	approved_bool	BOOLEAN,                                         -- Boolean to check if a request was approved.

	approve_dt 	TIMESTAMP                                             -- Approve date.  
);


CREATE TABLE transfer_info ( 
	transfer_fk	INTEGER REFERENCES transfer_req ( transfer_pk),  -- References the transfer request. 

	asset_fk        INTEGER REFERENCES assets ( asset_pk),           -- References assit that is going to be transfered 

	source_fk 	INTEGER REFERENCES facilities ( facility_pk),    -- References the source in transfer req, 

	load_dt 	TIMESTAMP, 				       	 -- Load time with date.
	
	dest_fk		INTEGER REFERENCES facilities ( facility_pk),	 -- References the dest in transfer req, 

	unload_dt	TIMESTAMP 					 -- Unload time with date. 
); 	


INSERT INTO facilities (facility_name, facility_code) VALUES ( 'DISPOSED', NULL);  --sets up a default facility DISPOSED 

															
