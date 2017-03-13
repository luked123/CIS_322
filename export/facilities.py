import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1], host= '127.0.0.1 ' , port='5432')
cur  = conn.cursor()

string = "fcode,common_name\n"

search = """
            SELECT facility_code, facility_name
            FROM facilities f; 
         """
cur.execute(search,)

res = cur.fetchall()

results = []; 

for row in res:
    e = dict()
    if row[0] != None: 
        e['fcode'] = row[0]
    else:
        e['fcode'] = "NULL"
    e['facility_name'] = row[1]
    results.append(e)

for row in results: 
    string = string + row['fcode'] + ',' + row['facility_name'] + '\n'

print(string, end="") 
