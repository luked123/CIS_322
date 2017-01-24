#Creator: Luke Donnelly
#Project: LOST 

#python script that reads legacy data and inserts data into the correct tables with correct relations

import csv
import os
import psycopg2
import sys

data = ['osnap_legacy/acquisitions.csv',            #0
        'osnap_legacy/convoy.csv',                  #1
        'osnap_legacy/DC_inventory.csv',            #2
        'osnap_legacy/HQ_inventory.csv',            #3
        'osnap_legacy/MB005_inventory.csv',         #4
        'osnap_legacy/NC_inventory.csv',            #5
        'osnap_legacy/product_list.csv',            #6
        'osnap_legacy/security_compartments.csv',   #7
        'osnap_legacy/security_levels.csv',         #8
        'osnap_legacy/SPNV_inventory.csv',          #9
        'osnap_legacy/transit.csv',                 #10
        'osnap_legacy/vendors.csv'                  #11
        ]
inventory_list = [  'osnap_legacy/DC_inventory.csv',
                    'osnap_legacy/HQ_inventory.csv',
                    'osnap_legacy/MB005_inventory.csv', 
                    'osnap_legacy/NC_inventory.csv',
                    'osnap_legacy/SPNV_inventory.csv'
                 ]


fcode_list = ['DC', 'HQ', 'MB005', 'NC', 'SPNV']
common_list = ['Washington, D.C.', 'HeadQuarters', 'MB005', 'National City', 'Sparks, NV']
index = 0

conn = psycopg2.connect(dbname = sys.argv[1], host = '127.0.0.1', port = int(sys.argv[2]))
cur = conn.cursor()

#sorts inventory assets and asigns them to correct facility
for rel_path in inventory_list:
    cur.execute("INSERT INTO facilities (fcode, common_name) VALUES (%s,%s)", (fcode_list[index], common_list[index],))

    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cur.execute("INSERT INTO products (description) VALUES (%s)", (row['product'],))
            cur.execute("SELECT product_pk FROM products WHERE description=%s", (row['product'],))
            product_pk = cur.fetchone()[0]
            cur.execute("INSERT INTO assets (asset_tag,product_fk) VALUES (%s,%s)", (row['asset tag'], product_pk,))
            cur.execute("SELECT asset_pk FROM assets WHERE asset_tag=%s", (row['asset tag'],))
            asset_pk = cur.fetchone()[0]
            cur.execute("SELECT facility_pk FROM facilities WHERE fcode=%s",(fcode_list[index],))
            facility_pk = cur.fetchone()[0]
            cur.execute("INSERT INTO asset_at (asset_fk, facility_fk) VALUES (%s,%s)", (asset_pk, facility_pk,))

    index += 1

#inserts security levels
script_dir = os.path.dirname(__file__)
rel_path = data[8]
abs_file_path = os.path.join(script_dir, rel_path)
with open(abs_file_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute("INSERT INTO levels (abbrv, comment) VALUES (%s,%s)" , (row['level'], row['description'],))

#inserts convoy info                
script_dir = os.path.dirname(__file__)
rel_path = data[1]
abs_file_path = os.path.join(script_dir, rel_path)
with open(abs_file_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute("INSERT INTO convoys (request, depart_dt, arrive_dt) VALUES (%s,%s,%s)" , (row['transport request #'], row['depart time'], row['arrive time'],))

#inserts compartments
script_dir = os.path.dirname(__file__)
rel_path = data[7]
abs_file_path = os.path.join(script_dir, rel_path)
with open(abs_file_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        cur.execute("INSERT INTO compartments (abbrv) VALUES (%s)" , (row['compartment_tag'],))

#data that did not fit format
cur.execute("INSERT INTO products (description) VALUES ('unobtainium')") 
cur.execute("INSERT INTO products (description) VALUES ('fuel')") 

conn.commit()

cur.close()
conn.close()
