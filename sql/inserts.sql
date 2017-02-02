INSERT INTO assets (asset_tag) VALUES('CA15467287');
INSERT INTO assets (asset_tag) VALUES('CA15467288');
INSERT INTO assets (asset_tag) VALUES('CA15467289');
INSERT INTO assets (asset_tag) VALUES('CA15467290');

INSERT INTO assets (asset_tag) VALUES('DC15467299');
INSERT INTO assets (asset_tag) VALUES('DC25467300');
INSERT INTO assets (asset_tag) VALUES('DC25467301');
INSERT INTO assets (asset_tag) VALUES('DC25467302');

INSERT INTO assets (asset_tag) VALUES('MB2222761');
INSERT INTO assets (asset_tag) VALUES('MB2222762');

INSERT INTO assets (asset_tag) VALUES('CA15467291');
INSERT INTO assets (asset_tag) VALUES('CA15467292');
INSERT INTO assets (asset_tag) VALUES('CA15467293');
INSERT INTO assets (asset_tag) VALUES('CA15467294');

INSERT INTO assets (asset_tag) VALUES('CA15467295');
INSERT INTO assets (asset_tag) VALUES('CA15467296');

INSERT INTO products (description) VALUES('1L H20');
INSERT INTO products (description) VALUES('notepad');
INSERT INTO products (description) VALUES('unobtainium');
INSERT INTO products (description) VALUES('fuel');
INSERT INTO products (description) VALUES('Zapper');
INSERT INTO products (description) VALUES('XJ 3000 scanner');
INSERT INTO products (description) VALUES('Olivine basalt');
INSERT INTO products (description) VALUES('Anorthosite');
INSERT INTO products (description) VALUES('breccias');
INSERT INTO products (description) VALUES('Red Lion');
INSERT INTO products (description) VALUES('Green Lion');
INSERT INTO products (description) VALUES('Blue Lion');
INSERT INTO products (description) VALUES('Yellow Lion');
INSERT INTO products (description) VALUES('50 mm film');
INSERT INTO products (description) VALUES('Atari ET video game cartridge');

UPDATE assets SET product_fk = 7 WHERE asset_pk = 1; 
UPDATE assets SET product_fk = 8 WHERE asset_pk = 2; 
UPDATE assets SET product_fk = 9 WHERE asset_pk = 3; 
UPDATE assets SET product_fk = 9 WHERE asset_pk = 4; 
UPDATE assets SET product_fk = 10 WHERE asset_pk = 5; 
UPDATE assets SET product_fk = 11 WHERE asset_pk = 6; 
UPDATE assets SET product_fk = 12 WHERE asset_pk = 7; 
UPDATE assets SET product_fk = 13 WHERE asset_pk = 8; 
UPDATE assets SET product_fk = 1 WHERE asset_pk = 9; 
UPDATE assets SET product_fk = 1 WHERE asset_pk = 10; 
UPDATE assets SET product_fk = 2 WHERE asset_pk = 11; 
UPDATE assets SET product_fk = 1 WHERE asset_pk = 12; 
UPDATE assets SET product_fk = 5 WHERE asset_pk = 13; 
UPDATE assets SET product_fk = 6 WHERE asset_pk = 14; 
UPDATE assets SET product_fk = 14 WHERE asset_pk = 15;
UPDATE assets SET product_fk = 15 WHERE asset_pk = 16;

INSERT INTO facilities (fcode, common_name) VALUES('HQ', 'Headquarters');
INSERT INTO facilities (fcode, common_name) VALUES('DC', 'Washington, D.C');
INSERT INTO facilities (fcode, common_name) VALUES('NC', 'National City'); 
INSERT INTO facilities (fcode, common_name) VALUES('SPNV', 'Sparks, NV');
INSERT INTO facilities (fcode, common_name) VALUES('MB005', 'MB 005');

INSERT INTO levels (abbrv, comment) VALUES('u', 'sensitive but unclassified');
INSERT INTO levels (abbrv, comment) VALUES('s', 'secret');
INSERT INTO levels (abbrv, comment) VALUES('ts', 'top secret');
INSERT INTO levels (abbrv, comment) VALUES('ss', '*REDACTED*');
INSERT INTO levels (abbrv, comment) VALUES('z', '*REDACTED*');

INSERT INTO compartments (abbrv, comment) VALUES('moon', '*REDACTED1*');
INSERT INTO compartments (abbrv, comment) VALUES('adm', '*REDACTED2*');
INSERT INTO compartments (abbrv, comment) VALUES('volt', '*REDACTED3*');
INSERT INTO compartments (abbrv, comment) VALUES('et', '*REDACTED4*');
INSERT INTO compartments (abbrv, comment) VALUES('lgm', '*REDACTED5*');
INSERT INTO compartments (abbrv, comment) VALUES('wpn', '*REDACTED6*');
INSERT INTO compartments (abbrv, comment) VALUES('nrg', '*REDACTED7*');

INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(1, 1, '1/7/2017', NULL); 
INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(2, 1, '1/7/2017', NULL);
INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(3, 1, '1/7/2017', NULL);
INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(4, 1, '1/7/2017', NULL);
INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(5, 2, '1/10/2017', NULL);
INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(6, 2, '1/10/2017', NULL);
INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(7, 2, '1/10/2017', NULL);
INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(8, 2, '1/10/2017', NULL);

INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(9, 5, '12/15/2016', '12/31/2016');
INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(10, 5, '12/15/2016', '12/31/2016');

INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(11, 3, '1/8/2017', '12/31/2016');
INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(12, 3, '1/8/2017', '12/31/2016');
INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(13, 3, '1/8/2017', '12/31/2017');
INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(14, 3, '1/8/2017', NULL);

INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(15, 4, '1/8/2017', NULL);
INSERT INTO asset_at( asset_fk, facility_fk, arrive_dt, depart_dt) VALUES(16, 4, '1/8/2017', NULL);

INSERT INTO facilities (fcode, common_name) VALUES('ST', 'Site 300');
INSERT INTO facilities (fcode, common_name) VALUES('GL', 'Groom Lake');
INSERT INTO facilities (fcode, common_name) VALUES('LA', 'Los Alamos, NM');

INSERT INTO convoys (request, source_fk, dest_fk, depart_dt, arrive_dt) VALUES('MB5696', 5, 1, '1/4/2017', '1/7/2017');
INSERT INTO convoys (request, source_fk, dest_fk, depart_dt, arrive_dt) VALUES('ST9776', 6, 3, '1/8/2017', '1/8/2017');
INSERT INTO convoys (request, source_fk, dest_fk, depart_dt, arrive_dt) VALUES('GL2334', 7, 4, '1/8/2017', '1/8/2017');
INSERT INTO convoys (request, source_fk, dest_fk, depart_dt, arrive_dt) VALUES('LA1213', 8, 2, '1/10/2017', '1/10/2017');

INSERT INTO asset_on (asset_fk, convoy_fk) VALUES( 1, 1);
INSERT INTO asset_on (asset_fk, convoy_fk) VALUES( 2, 1);
INSERT INTO asset_on (asset_fk, convoy_fk) VALUES( 3, 1);
INSERT INTO asset_on (asset_fk, convoy_fk) VALUES( 4, 1);

INSERT INTO asset_on (asset_fk, convoy_fk) VALUES( 11, 2);
INSERT INTO asset_on (asset_fk, convoy_fk) VALUES( 12, 2);
INSERT INTO asset_on (asset_fk, convoy_fk) VALUES( 13, 2);
INSERT INTO asset_on (asset_fk, convoy_fk) VALUES( 14, 2);

INSERT INTO asset_on (asset_fk, convoy_fk) VALUES( 15, 3);
INSERT INTO asset_on (asset_fk, convoy_fk) VALUES( 16, 3);

INSERT INTO asset_on (asset_fk, convoy_fk) VALUES( 5, 4);
INSERT INTO asset_on (asset_fk, convoy_fk) VALUES( 6, 4);
INSERT INTO asset_on (asset_fk, convoy_fk) VALUES( 7, 4);
INSERT INTO asset_on (asset_fk, convoy_fk) VALUES( 8, 4);

