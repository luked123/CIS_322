import sys
import psycopg2
import time
from datetime import date

conn = psycopg2.connect(dbname=sys.argv[1], host= '127.0.0.1 ' , port='5432')
cur  = conn.cursor()

string = "asset_tag,request_by,request_dt,approve_by, approve_dt, source, destination, load_dt, unload_dt\n"

search = """
            SELECT a.asset_tag, a.asset_desc, f.facility_code, t.arrival_dt, t.dispose_dt
            FROM assets a
            JOIN facilities f
            ON a.asset_at = f.facility_pk
            JOIN transit t 
            ON asset_fk = asset_pk;
         """
cur.execute(search,)

res = cur.fetchall()

results = []; 

for row in res:
    e = dict()
    e['asset_tag']   = row[0]
    e['description'] = row[1]
    if row[2] != None:
        e['fcode'] = row[2]
    else:
        e['fcode'] = "NULL"
    if row[3] != None:
        e['acquired'] = row[3].strftime('%Y-%m-%d')
    else:
        e['acquired'] = "NULL" 
    if row[4] != None: 
         e['disposed'] = row[4].strftime('%Y-%m-%d')
    else:
        e['disposed'] = "NULL"

    results.append(e)

for row in results: 
    string = string + row['asset_tag'] + ',' + row['description'] + ',' + row['fcode'] + ',' +  row['acquired'] +  ',' + row['disposed'] + '\n'

print(string, end="") 
