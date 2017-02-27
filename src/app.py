from flask import Flask, render_template, request, url_for, redirect, session
from config import dbname, dbhost, dbport
import datetime 
import json
import psycopg2 

#Web application for LOST database
# Creator: Luke Donnelly


app = Flask(__name__)
app.secret_key = "A7/62%![1280Ta1A"


conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
cur = conn.cursor()


#login page
@app.route('/')
@app.route('/login', methods=('POST', 'GET', ))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 

        if username == "":                                  # cannot enter blank username
            error = "username or password do not match"
            return redirect(url_for('error', error=error)) 
        if password == "":                                  # cannot enter blank password
            error = "username or password do not match"
            return redirect(url_for('error', error=error)) 

        check = """                                         
                    SELECT username, password 
                    FROM users
                    WHERE username = %s AND password = %s; 
                """                                         #SQL query
      
        cur.execute(check,(username, password,))
        res = cur.fetchall()
        
                           
        if not res:                                         # check if response is an empty list, if it is there was no match
            error = "username or password do not match"
            return redirect(url_for('error', error=error)) 
        else:
            session['username'] = username                  # there was match, start session
            session['logged_in'] = True                     # logged in
            return redirect(url_for('dashboard'))

    return render_template('login.html') 


# dashboard page
@app.route('/dashboard')
def dashboard():
    if session.get('logged_in') != True:                    # must be logged in to be in dashboard
        return redirect(url_for('not_logged'))
    return render_template('dashboard.html') 


# create_user page
@app.route('/create_user', methods=('POST', 'GET', ))
def create_user():
    
    if request.method=='POST':
        username = request.form['username']                 
        password = request.form['password']
        role     = request.form['role'] 
        
        if username == "":
            error = "username cannot be blank"
            return redirect(url_for('error', error=error))  
        if " " in username: 
            error = "usernames cannot have spaces" 
            return redirect(url_for('error', error=error))  
        if password == "":
            error = "password cannot be empty"
            return redirect(url_for('error', error=error))  
        if " " in username: 
            error = "passwords cannot have spaces"
            return redirect(url_for('error', error=error))
            
        search = """
                    SELECT username
                    FROM users
                    WHERE username = %s; 
                 """                                         # SQL query
       
        cur.execute(search,(username,))
        res = cur.fetchall()

        if not res:                                         # if response is an empty list, insert username/password pair   
             create = """
                        INSERT INTO users (username, password) 
                        VALUES ( %s, %s);
                     """                                     # SQL query
             cur.execute(create,(username, password,))
    
             search = """
                        SELECT role 
                        FROM roles
                        WHERE role = %s; 
                     """    
             cur.execute(search,(role,))
             res = cur.fetchall()

             if not res: 
                     create = """ 
                                 INSERT INTO roles (role) 
                                 VALUES (%s); 
                              """
                     cur.execute(create,(role,))

             update = """
                            UPDATE users 
                            SET role_fk = (SELECT role_pk FROM roles WHERE role = %s) 
                            WHERE username = %s; 
                      """

             cur.execute(update,(role, username,))
             conn.commit()

             return render_template('added.html')

        else:                                                     
             error = "username already exists"
             return redirect(url_for('error', error=error)) 
    
    session['roles'] = ["Logistics Officer", "Facilities Officer"] 

    return render_template('create_user.html')


# add facility page
@app.route('/add_facility', methods=('POST','GET', ))
def add_facility(): 
    if request.method == 'POST':
        facility_name = request.form['facility_name']
        facility_code = request.form['facility_code'] 
        
        if facility_name == "":
            error = "facility common name cannot be blank"
            return redirect(url_for('error', error=error))  
        
        if facility_code == "":
            error = "facility code cannot be blank"
            return redirect(url_for('error', error=error))  

        search = """
                    SELECT facility_name
                    FROM facilities
                    WHERE facility_name = %s OR facility_code =%s;  
                 """
        cur.execute(search,(facility_name,facility_code,))
        res = cur.fetchall()

        if not res: 
            create = """
                        INSERT INTO facilities (facility_name, facility_code)
                        VALUES (%s, %s); 
                     """
            cur.execute(create,(facility_name,facility_code,))
            conn.commit()
            return redirect(url_for('add_facility'))
        else:
            error="facility name or facility code already exists"
            return redirect(url_for('error', error=error))

    search = """
                SELECT facility_name, facility_code
                FROM facilities; 
             """
    cur.execute(search)
    
    res = cur.fetchall()
    facility_table = []

    for row in res:
        if row[0] == "DISPOSED":
            continue
        e = dict()
        e['facility_name'] = row[0]
        e['facility_code'] = row[1]
        facility_table.append(e)

    session['facility_table'] = facility_table

    return render_template('add_facility.html') 

# add asset page
@app.route('/add_asset', methods=('POST','GET',))
def add_asset(): 
    if request.method == 'POST':
        asset_tag  = request.form['asset_tag']
        asset_desc = request.form['asset_desc'] 
        facility_name = request.form['facility_name'] 
        arrive_dt     = request.form['arrive_dt'] 
        
        if asset_tag == "": 
            error="asset tag cannot be blank"
            return redirect(url_for('error', error=error))
        if arrive_dt =="":
            error="arrival date cannot be blank" 
            return redirect(url_for('error', error=error))

        search = """
                    SELECT asset_tag 
                    FROM assets
                    WHERE asset_tag = %s
                 """

        cur.execute(search,(asset_tag,))
        res = cur.fetchall()

        if not res: 
            create = """
                        INSERT INTO assets (asset_tag, asset_desc, asset_at) 
                        VALUES (%s, %s, (SELECT facility_pk FROM facilities WHERE facility_name = %s)); 

                        INSERT INTO transit (asset_fk, final_fk, arrival_dt) 
                        VALUES ((SELECT asset_pk FROM assets WHERE asset_tag = %s),
                                (SELECT facility_pk FROM facilities WHERE facility_name = %s),
                                %s); 
                    """
            cur.execute(create,(asset_tag,asset_desc,facility_name,asset_tag,facility_name,arrive_dt,))
            conn.commit()

            return redirect(url_for('add_asset'))
        else: 
            error="Asset already exists" 
            return redirect(url_for('error', error=error)) 

    search = """
                SELECT facility_name 
                FROM facilities; 
             """
    cur.execute(search)

    res = cur.fetchall()
    facilities = []
    
    for row in res:
        if row[0] == 'DISPOSED':
            continue

        facilities.append(row[0]) 

    session['facilities'] = facilities

    search = """
                SELECT a.asset_tag, f.facility_name, a.asset_desc
                FROM assets a
                JOIN facilities f
                ON asset_at = facility_pk; 
             """
    cur.execute(search)

    res = cur.fetchall()
    asset_table = []

    for row in res:
        e = dict()
        e['asset_tag']  = row[0]
        e['asset_at']   = row[1]
        e['asset_desc'] = row[2] 
        asset_table.append(e)

    session['asset_table'] = asset_table

    return render_template('add_asset.html')


# dispose asset page
@app.route('/dispose_asset', methods=('POST', 'GET',))
def dispose_asset():

    if request.method == 'POST':
        asset_tag = request.form['asset_tag']
        dispose_dt = request.form['dispose_dt']

        if asset_tag == "":
            error = "asset tag cannot be blank"
            return redirect(url_for('error', error=error))

        if dispose_dt == "": 
            error = "dipose date cannot be blank"
            return redirect(url_for('error', error=error)) 

        search = """
                    SELECT a.asset_tag, f.facility_name 
                    FROM assets a
                    JOIN facilities f
                    ON a.asset_at = f.facility_pk
                    WHERE asset_tag = %s; 
                 """

        cur.execute(search,(asset_tag,))
        res = cur.fetchone()

        if not res:
            error = "asset tag does not exist" 
            return redirect(url_for('error', error=error)) 
        
        if res[1] == "DISPOSED":
            error = "asset was already disposed"
            return redirect(url_for('error', error=error)) 
        else:
            change = """
                        UPDATE assets
                        SET asset_at = (SELECT facility_pk FROM facilities WHERE facility_name = 'DISPOSED')
                        WHERE asset_tag = %s; 

                        UPDATE transit
                        SET final_fk = (SELECT facility_pk FROM facilities WHERE facility_name = 'DISPOSED'),
                            arrival_dt = NULL,
                            depart_dt = %s
                        WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = %s);
                     """
            cur.execute(change,(asset_tag, dispose_dt,asset_tag,))
            conn.commit()

            return redirect(url_for('dashboard')) 

    return render_template('dispose_asset.html')

# asset report page
@app.route('/asset_report', methods=('POST', 'GET',))
def asset_report():
    if request.method == 'POST':
        facility_name = request.form['facility_name']
        date          = request.form['date'] 
    
        if date == "":
            error = "date cannot be blank"
            return redirect(url_for('error', error=error)) 
    
        if facility_name == "": 
            search = """
                        SELECT a.asset_tag, a.asset_desc, f.facility_name, t.arrival_dt, t.depart_dt
                        FROM assets a 
                        JOIN facilities f
                        ON a.asset_at = f.facility_fk
                        JOIN transit t
                        WHERE t.arrival_dt = %s OR t.depart_dt = %s;
                    """

            cur.execute(search,(date,date,))
            res = cur.fetchall() 
        
            asset_report_table = [] 
            for row in res: 
                e = dict()
                e['asset_tag']     = row[0]
                e['asset_desc']    = row[1]
                e['facility_name'] = row[2]
                e['arrival_dt']    = row[3]
                e['depart_dt']     = row[4] 
                asset_report_table.append(e)

            session['asset_report_table'] =asset_report_table

            return render_template('asset_report.html')

        else:
            search = """
                        SELECT a.asset_tag, a.asset_desc, f.facility_name, t.arrival_dt, t.depart_dt
                        FROM assets a 
                        JOIN facilities f
                        ON a.asset_at = f.facility_fk
                        JOIN transit t
                        WHERE f.facilty_name = %s AND (t.arrival_dt = %s OR t.depart_dt = %s);
                    """

            cur.execute(search,(facility_name,date,date,))
            res = cur.fetchall() 
            asset_report_table = []

            for row in res: 
                e = dict()
                e['asset_tag']     = row[0]
                e['asset_desc']    = row[1]
                e['facility_name'] = row[2]
                e['arrival_dt']    = row[3]
                e['depart_dt']     = row[4] 
            

            session['asset_report_table'] = asset_report_table

            return render_template('asset_report.html')

    return render_template('asset_report.html')

# logout page
@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')


# not_logged page
@app.route('/not_logged')
def not_logged():
    return render_template('not_logged.html')


# error page
@app.route('/error')
def error():
    return render_template('error.html', error=request.args.get('error'))


