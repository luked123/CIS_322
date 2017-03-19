import sys
import psycopg2

# Prepares the facilities CSV file to be exported from the database. 

conn = psycopg2.connect(dbname=sys.argv[1], host= '127.0.0.1 ' , port='5432')
cur  = conn.cursor()

string = "fcode,common_name\n"          # Column headers. 

search = """
            SELECT facility_code, facility_name
            FROM facilities f; 
         """
cur.execute(search,)

res = cur.fetchall()

results = []; 

for row in res:
    e = dict()
    e['fcode']         = row[0]
    e['facility_name'] = row[1]
    results.append(e)

for row in results: 
    string = string + row['fcode'] + ',' + row['facility_name'] + '\n'

print(string, end="") 
