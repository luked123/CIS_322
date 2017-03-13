import sys
import psycopg2

conn = psycopg2.connect(dbname=sys.argv[1], host= '127.0.0.1 ' , port='5432')
cur  = conn.cursor()

string = "username,password,role,active\n"

search = """
            SELECT u.username, u.password, r.role, u.active
            FROM users u
            JOIN roles r
            ON u.role_fk = r.role_pk;
         """
cur.execute(search,)

res = cur.fetchall()

results = []; 

for row in res:
    e = dict()
    e['username'] = row[0]
    e['password'] = row[1]
    e['role']     = row[2]
    if row[3] == True: 
        e['active'] = 'True'
    else:
        e['active'] = 'False' 
    results.append(e)

for row in results: 
    string = string + row['username'] + ',' + row['password'] + ',' + row['role'] + ',' + row['active'] + '\n'

print(string, end="") 
