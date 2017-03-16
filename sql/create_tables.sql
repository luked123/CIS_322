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

	asset_desc	TEXT, 						-- Asset description

	initial_fk     	INTEGER REFERENCES facilities ( facility_pk),   -- Initial facility asset was created

	initial_dt      DATE, 						-- Date asset was initially created

	dispose_dt	DATE						-- Date asset was disposed if applicable 
); 

CREATE TABLE asset_at (
	asset_fk 	INTEGER REFERENCES assets ( asset_pk),           -- References asset
	
	facility_fk 	INTEGER REFERENCES facilities ( facility_pk),	 -- Where the asset is at 

	arrival_dt	DATE,                                            -- Date it arrived at facility

	depart_dt 	DATE                                             -- Date it departed facility

	tranfering 	BOOLEAN						 -- Asset is transfering

	transfered 	BOOLEAN						 -- Asset was transfered
); 


CREATE TABLE transfer_req (
	transfer_pk 	SERIAL PRIMARY KEY,				 -- Transfer request should be differentiated.

	log_fk 		INTEGER REFERENCES users ( user_pk),             -- Logistic officer making the request.

	asset_fk	INTEGER REFERENCES assets ( asset_pk),		 -- Asset to be transfered. 

	source_fk  	INTEGER REFERENCES facilities ( facility_pk),    -- Where the asset is located currently.

	dest_fk		INTEGER REFERENCES facilities ( facility_pk),    -- Where the asset is requested to go.

	req_dt		TIMESTAMP, 					 -- Date request was made. 

	fac_fk		INTEGER REFERENCES users ( user_pk),             -- Facilities officer that approve/ deny request.   

	approved_bool	BOOLEAN,                                         -- Boolean to check if a request was approved.

	approve_dt 	TIMESTAMP                                        -- Approve date.  
);


CREATE TABLE transfer_info ( 
	transfer_fk	INTEGER REFERENCES transfer_req ( transfer_pk),  -- References the transfer request. 

	asset_fk        INTEGER REFERENCES assets ( asset_pk),           -- References asset that is going to be transfered 

	source_fk 	INTEGER REFERENCES facilities ( facility_pk),    -- References the source in transfer req, 

	load_dt 	TIMESTAMP, 				       	 -- Load time with date.
	
	dest_fk		INTEGER REFERENCES facilities ( facility_pk),	 -- References the dest in transfer req, 

	unload_dt	TIMESTAMP 					 -- Unload time with date. 
); 	



															
