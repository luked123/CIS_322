import csv
import os
import psycopg2
import sys

conn = psycopg2.connect(dbname = sys.argv[1], host='127.0.0.1', port='5432')
cur = conn.cursor()

# paths
path = str(sys.argv[2])
users_path = path + '/users.csv' 
facilities_path = path + '/facilities.csv'
assets_path = path + '/assets.csv'
transfers_path = path + '/transfers.csv'

# Since only two roles inserting these in manually
# Will make everything fall in place easier
roles = ['Logistics Officer', 'Facilities Officer']

for role in roles:
    cur.execute("INSERT INTO roles (role) VALUES (%s)",( role,))

with open(users_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        users = """
                    INSERT INTO users (username, password, role_fk, active) 
                    VALUES (%s, %s, (SELECT role_pk FROM roles WHERE role = %s), %s);
                """
        cur.execute(users, (row['username'],row['password'],row['role'],row['active'],))
csvfile.close()


with open(facilities_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        facilities = """
                         INSERT INTO facilities (facility_code, facility_name) 
                         VALUES (%s, %s);
                     """
        cur.execute(facilities, (row['fcode'], row['common_name'],))
csvfile.close()


with open(assets_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        assets = """
                     INSERT INTO assets (asset_tag, asset_desc, initial_fk, initial_dt, dispose_dt) 
                     VALUES (%s, %s, (SELECT facility_pk FROM facilities WHERE facility_code = %s), %s, %s);
                 """
        if row['disposed'] == "NULL":
            row['disposed'] = None
        cur.execute(assets,(row['asset_tag'],row['description'],row['facility'],row['acquired'],row['disposed'],))

        asset_at = """
                     INSERT INTO asset_at (asset_fk, facility_fk, arrival_dt, requested, transfering, transfered)
                     VALUES ((SELECT asset_pk FROM assets WHERE asset_tag = %s), 
                             (SELECT facility_pk FROM facilities WHERE facility_code = %s), 
                             %s, 'false', 'false', 'false'); 
                   """   
        cur.execute(asset_at,(row['asset_tag'],row['facility'],row['acquired'],))

with open(transfers_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        transfer_req = """
                            INSERT INTO transfer_req (log_fk, asset_fk, source_fk, dest_fk,req_dt, 
                            fac_fk, approved_bool, approve_dt) 
                            VALUES ((SELECT user_pk FROM users WHERE username = %s), 
                                    (SELECT asset_pk FROM assets WHERE asset_tag = %s),
                                    (SELECT facility_pk FROM facilities WHERE facility_code = %s),
                                    (SELECT facility_pk FROM facilities WHERE facility_code = %s),
                                    %s, 
                                    (SELECT user_pk FROM users WHERE username = %s), 
                                    'true', 
                                    %s);
                        """
        cur.execute(transfer_req,(row['request_by'], row['asset_tag'], row['source'], row['destination'], row['request_dt'], row['approve_by'], row['approve_dt'],))

        transfer_info = """
                            INSERT INTO transfer_info (transfer_fk, asset_fk, source_fk, load_dt, dest_fk, unload_dt)
                            VALUES ((SELECT transfer_pk FROM transfer_req 
                                     WHERE log_fk        = (SELECT user_pk FROM users WHERE username = %s) AND
                                           asset_fk      = (SELECT asset_pk FROM assets WHERE asset_tag = %s) AND
                                           source_fk     = (SELECT facility_pk FROM facilities WHERE facility_code = %s) AND
                                           dest_fk       = (SELECT facility_pk FROM facilities WHERE facility_code = %s) AND
                                           req_dt        =  %s AND 
                                           fac_fk        = (SELECT user_pk FROM users WHERE username = %s) AND
                                           approved_bool = 'true' AND
                                           approve_dt    = %s),
                                     (SELECT asset_pk FROM assets WHERE asset_tag = %s),
                                     (SELECT facility_pk FROM facilities WHERE facility_code = %s), 
                                     %s,
                                     (SELECT facility_pk FROM facilities WHERE facility_code = %s),
                                     %s);
                        """
        cur.execute(transfer_info,(row['request_by'], row['asset_tag'], row['source'], row['destination'], row['request_dt'], row['approve_by'], row['approve_dt'], row['asset_tag'], row['source'], row['load_dt'], row['destination'], row['unload_dt'],))
        
        update_asset = """
                            UPDATE asset_at 
                            SET depart_dt = %s, requested= 'true', transfering = 'true', transfered = 'true'
                            WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = %s) AND 
                                  requested = 'false' AND transfering = 'false' AND transfered = 'false'; 

                            INSERT INTO asset_at (asset_fk, facility_fk, arrival_dt, requested, transfering, transfered)
                            VALUES ((SELECT asset_pk FROM assets WHERE asset_tag = %s), 
                                    (SELECT facility_pk FROM facilities WHERE facility_code = %s),
                                    %s, 'false', 'false', 'false'); 
                        """

        cur.execute(update_asset,(row['load_dt'], row['asset_tag'], row['asset_tag'], row['destination'], row['unload_dt'],))

csvfile.close()

conn.commit()
conn.close()
