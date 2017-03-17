import sys
import psycopg2
import time
from datetime import date

conn = psycopg2.connect(dbname=sys.argv[1], host= '127.0.0.1 ' , port='5432')
cur  = conn.cursor()

string = "asset_tag,request_by,request_dt,approve_by,approve_dt,source,destination,load_dt,unload_dt\n"

search = """
            SELECT a.asset_tag, lo.username, tr.req_dt, fo.username, 
            tr.approve_dt, s.facility_code, d.facility_code, ti.load_dt, ti.unload_dt 
            FROM transfer_info ti
            JOIN assets a
            ON ti.asset_fk = a.asset_pk
            JOIN transfer_req tr
            ON ti.transfer_fk = tr.transfer_pk
            JOIN users lo
            ON tr.log_fk    = lo.user_pk
            JOIN users fo  
            ON tr.fac_fk    = fo.user_pk 
            JOIN facilities s
            ON ti.source_fk = s.facility_pk
            JOIN facilities d
            ON ti.dest_fk   = d.facility_pk
         """
cur.execute(search,)

res = cur.fetchall()

results = []; 

for row in res:
    e = dict()
    e['asset_tag']          = row[0]
    e['logistics_officer']  = row[1]
    e['request_dt']         = str(row[2])
    e['facilities_officer'] = row[3]
    e['approve_dt']         = str(row[4])
    e['source']             = row[5]
    e['dest']               = row[6]
    e['load']               = str(row[7])
    e['unload']             = str(row[8])

    results.append(e)

for row in results: 
    string = string + row['asset_tag'] + ',' + row['logistics_officer'] + ',' + row['request_dt'] + ',' +  row['facilities_officer'] +  ',' + row['approve_dt'] + ',' + row['source'] + ',' + row['dest'] + ',' + row['load'] + ',' + row['unload'] + '\n'

print(string, end="") 
