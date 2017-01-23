CREATE TABLE products( 
	product_pk 	SERIAL PRIMARY KEY, 
	vendor		TEXT, 
	description 	TEXT, 
	alt_description TEXT
); 

CREATE TABLE assets(
	asset_pk 	SERIAL PRIMARY KEY, 
	product_fk 	INTEGER REFERENCES products (product_pk) NOT NULL, 
	asset_tag	TEXT, 
	description 	TEXT, 
	alt_description TEXT
); 

CREATE TABLE vehichles( 
	vehichle_pk	SERIAL PRIMARY KEY,
	asset_fk 	INTEGER REFERENCES assets (asset_pk) NOT NULL
); 

CREATE TABLE facilities(
	facility_pk 	SERIAL PRIMARY KEY, 
	fcode 		TEXT, 
	common_name 	TEXT, 
	location 	TEXT
); 

CREATE TABLE asset_at(
	asset_fk 	INTEGER REFERENCES assets (asset_pk) NOT NULL,
	facility_fk  	INTEGER REFERENCES facilities (facility_pk) NOT NULL,
	arrive_dt 	DATE, 
	depart_dt 	DATE
); 

CREATE TABLE convoys(
	convoy_pk	SERIAL PRIMARY KEY,
	request 	TEXT, 
	source_fk	INTEGER REFERENCES facilities (facility_pk) NOT NULL, 
	dest_fk		INTEGER REFERENCES facilities (facility_pk) NOT NULL, 
	depart_dt	TIMESTAMP,
	arrive_dt	TIMESTAMP
); 

CREATE TABLE used_by(
	vehichle_fk	INTEGER REFERENCES vehichles (vehichle_pk) NOT NULL,
	convoy_fk	INTEGER REFERENCES convoys (convoy_pk) NOT NULL
);

CREATE TABLE asset_on(
	asset_fk	INTEGER REFERENCES assets (asset_pk) NOT NULL, 
	convoy_fk	INTEGER REFERENCES convoys (convoy_pk) NOT NULL,
	load_dt 	DATE, 
	unload_dt	DATE
); 

CREATE TABLE users(
	user_pk 	SERIAL PRIMARY KEY, 
	username 	TEXT, 
	active 		BOOLEAN
);

CREATE TABLE roles(
	role_pk 	SERIAL PRIMARY KEY, 
	title 		TEXT
);

CREATE TABLE user_is(
	user_fk 	INTEGER REFERENCES users (user_pk) NOT NULL, 
	role_fk 	INTEGER REFERENCES roles (role_pk) NOT NULL
); 

CREATE TABLE user_supports(
	user_fk 	INTEGER REFERENCES users (user_pk) NOT NULL,
	facility_fk 	INTEGER REFERENCES facilities (facility_pk) NOT NULL
);

CREATE TABLE levels(
	level_pk	SERIAL PRIMARY KEY,
	abbrv 		TEXT, 
	comment 	TEXT
); 

CREATE TABLE compartments(
	compartment_pk 	SERIAL PRIMARY KEY,
	abbrv 		TEXT,
	comment 	TEXT
); 

CREATE TABLE security_tags(
	tag_pk		SERIAL PRIMARY KEY,
	level_fk 	INTEGER REFERENCES levels (level_pk) NOT NULL,
	compartment_fk	INTEGER REFERENCES compartments (compartment_pk) NOT NULL,
	user_fk 	INTEGER REFERENCES users (user_pk) NOT NULL, 
	product_fk 	INTEGER REFERENCES products (product_pk) NOT NULL, 
	asset_fk 	INTEGER REFERENCES assets (asset_pk) NOT NULL
); 
