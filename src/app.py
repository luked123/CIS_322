from flask import Flask, render_template, request, url_for, redirect, session
from config import dbname, dbhost, dbport
from datetime import date
import json
import psycopg2 

#Web application for LOST database
# Creator: Luke Donnelly


app = Flask(__name__)
app.secret_key = "A7/62%![1280Ta1A"

conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
cur = conn.cursor()


# login page.
@app.route('/')
@app.route('/login', methods=('POST', 'GET', ))
def login():
    # POST method.
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 

        if username == "":                                    # Cannot enter blank username.
            error = "username or password do not match"
            return redirect(url_for('error', error=error)) 
        if password == "":                                    # Cannot enter blank password.
            error = "username or password do not match"
            return redirect(url_for('error', error=error)) 

        check = """                                         
                    SELECT u.username, r.role, u.password
                    FROM users u
                    JOIN roles r
                    ON u.role_fk = r.role_pk
                    WHERE u.username = %s AND u.password = %s; 
                """                                            # SQL checks the database for matching username and password.
        cur.execute(check,(username, password,))
        res = cur.fetchone()
                           
        if not res:                                           # Check if response is an empty list, if it is there was no match.
            error = "username or password do not match"
            return redirect(url_for('error', error=error)) 
        else:
            session['username']  = res[0]                    # There was a match, start session.
            session['user_role'] = res[1]                    # Users role. 
            session['logged_in'] = True                      # Logged in. 
            return redirect(url_for('dashboard'))
    
    #GET method.
    return render_template('login.html') 


# dashboard page.
@app.route('/dashboard')
def dashboard():
    if session.get('logged_in') != True:                    # Must be logged in to visit this page. 
        return redirect(url_for('not_logged'))

    # GET method. 
    return render_template('dashboard.html') 


# create_user page.
@app.route('/create_user', methods=('POST', 'GET', ))
def create_user():
    # POST method. 
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
        
        check = """
                    SELECT role 
                    FROM roles
                    WHERE role = %s; 
                """                                             # SQL check if role is in DB
        cur.execute(check,(role,))
        res = cur.fetchone()

        if not res: 
            create = """
                        INSERT INTO roles (role)
                        VALUES (%s); 
                     """                                        # SQL create role 
            cur.execute(create,(role,))
            conn.commit()

        search = """
                    SELECT username
                    FROM users
                    WHERE username = %s; 
                 """                                             # SQL searchs database for username entered.
        cur.execute(search,(username,))
        res = cur.fetchone()

        if not res:                                              # If response is an empty list, insert username/password pair.
             create = """
                        INSERT INTO users (username, password) 
                        VALUES ( %s, %s);
                     """                                         # SQL create username / password pair.
             cur.execute(create,(username, password,))
             conn.commit()

             update = """
                            UPDATE users 
                            SET role_fk = (SELECT role_pk FROM roles WHERE role = %s) 
                            WHERE username = %s; 
                      """                                        # SQL updates user with correct role. 

             cur.execute(update,(role, username,))              
             conn.commit()
             return render_template('added.html')
        else:                                                     
             error = "username already exists"
             return redirect(url_for('error', error=error)) 

    # GET method
    session['roles'] = ["Logistics Officer", "Facilities Officer"]     # Current roles at LOST DB.
    return render_template('create_user.html')


# add_facility page.
@app.route('/add_facility', methods=('POST','GET', ))
def add_facility():
    if session.get('logged_in') != True:                               # Must be logged in to visit this page. 
        return redirect(url_for('not_logged'))

    # POST method.
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
                 """                                                   #SQL search DB for matching facility names.

        cur.execute(search,(facility_name,facility_code,))
        res = cur.fetchall()

        if not res:                                                            # If no match, create facility.
            create = """
                        INSERT INTO facilities (facility_name, facility_code)
                        VALUES (%s, %s); 
                     """                                                        # SQL create facility.
            cur.execute(create,(facility_name,facility_code,))
            conn.commit()
            return redirect(url_for('add_facility'))

        else:
            error="facility name or facility code already exists"                # Match, do not create facility.
            return redirect(url_for('error', error=error))

    # GET method. 
    search = """
                SELECT facility_name, facility_code
                FROM facilities; 
            """                                              # SQL search for all current facilities.
    cur.execute(search)
    res = cur.fetchall()

    facility_table = []

    for row in res:
        if row[0] == "DISPOSED":                             # Don't display disposed facility. 
            continue
        e = dict()
        e['facility_name'] = row[0]
        e['facility_code'] = row[1]
        facility_table.append(e)

    session['facility_table'] = facility_table               

    return render_template('add_facility.html') 


# add_asset page.
@app.route('/add_asset', methods=('POST','GET',))
def add_asset():
    if session.get('logged_in') != True:                    # Must be logged in to visit this page.
        return redirect(url_for('not_logged'))

    #POST method. 
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

        check = """
                    SELECT asset_tag 
                    FROM assets
                    WHERE asset_tag = %s
                 """                                       # SQL check if asset tag is not a duplicate. 
        cur.execute(check,(asset_tag,))
        res = cur.fetchall()

        if not res:                                        # No match, create asset.   
            create = """
                        INSERT INTO assets (asset_tag, asset_desc, asset_at) 
                        VALUES (%s, %s, (SELECT facility_pk FROM facilities WHERE facility_name = %s)); 

                        INSERT INTO transit (asset_fk, final_fk, arrival_dt) 
                        VALUES ((SELECT asset_pk FROM assets WHERE asset_tag = %s),
                                (SELECT facility_pk FROM facilities WHERE facility_name = %s),
                                %s); 
                    """                                                                                    # SQL create asset. 
            cur.execute(create,(asset_tag,asset_desc,facility_name,asset_tag,facility_name,arrive_dt,))
            conn.commit()
            return redirect(url_for('add_asset'))
        else:                                                         # Match, do not create asset. 
            error="Asset already exists" 
            return redirect(url_for('error', error=error)) 

    # GET method.
    search = """
                SELECT facility_name 
                FROM facilities; 
             """                                                      # SQL search for every facility in DB.
    cur.execute(search)
    res = cur.fetchall()
    
    facilities = []
    
    for row in res:
        if row[0] == 'DISPOSED':
            continue
        facilities.append(row[0]) 

    session['facilities'] = facilities                                 # Used for select drop down menu in html. 

    search = """
                SELECT a.asset_tag, f.facility_name, a.asset_desc
                FROM assets a
                JOIN facilities f
                ON asset_at = facility_pk; 
             """                                                       # SQL search for every asset in DB.
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


# dispose_asset page. 
@app.route('/dispose_asset', methods=('POST', 'GET',))
def dispose_asset():
    if session.get('logged_in') != True:                    # must be logged in to visit this page
        return redirect(url_for('not_logged'))
    if session['user_role'] != "Logistics Officer":
        error = "Only Logistics Officers have access to this page"
        return redirect(url_for('error', error=error))

    #POST method.
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
                 """                                             # SQL search DB for asset tag. 
        cur.execute(search,(asset_tag,))                    
        res = cur.fetchone()

        if not res:                                              # No match, do nothing.
            error = "asset tag does not exist" 
            return redirect(url_for('error', error=error)) 
        if res[1] == "DISPOSED":                                 # Disposed already, do nothing. 
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
                     """                                                                     #SQL change asset to disposed. 
            cur.execute(change,(asset_tag, dispose_dt,asset_tag,))
            conn.commit()
            return redirect(url_for('dashboard')) 
    
    # GET method. 
    return render_template('dispose_asset.html')


# asset_report page.
@app.route('/asset_report', methods=('POST', 'GET',))
def asset_report():
    if session.get('logged_in') != True:                    # Must be logged in to visit this page. 
        return redirect(url_for('not_logged'))

    # POST method.
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
                        ON a.asset_at = f.facility_pk
                        JOIN transit t
                        ON a.asset_pk = t.asset_fk
                        WHERE t.arrival_dt = %s OR t.depart_dt = %s;
                    """                                                 # SQL search assets matching date in all facilities.
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

        else:                                                       # Specific facility name. 
            search = """
                        SELECT a.asset_tag, a.asset_desc, f.facility_name, t.arrival_dt, t.depart_dt
                        FROM assets a 
                        JOIN facilities f
                        ON a.asset_at = f.facility_pk
                        JOIN transit t
                        ON a.asset_pk = t.asset_fk
                        WHERE f.facility_name = %s AND (t.arrival_dt = %s OR t.depart_dt = %s);
                    """                                              # SQL search assets in specific facility matching date. 
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
                asset_report_table.append(e) 

            session['asset_report_table'] = asset_report_table

            return render_template('asset_report.html')
    
    #GET method
    search = """
                SELECT facility_name 
                FROM facilities; 
             """                                                      # SQL search for every facility in DB.
    cur.execute(search)
    res = cur.fetchall()

    facilities = []
    
    for row in res:
        if row[0] == 'DISPOSED':
            continue
        facilities.append(row[0]) 

    session['facilities'] = facilities                                 # Used for select drop down menu in html.

    return render_template('asset_report.html')


# transfer_report page. 
@app.route('/transfer_report')
def transfer_report():
    return


# transfer_req page. 
@app.route('/transfer_req', methods=('POST','GET',))
def transfer_req(): 
    if session.get('logged_in') != True:                    # Must be logged in to visit this page. 
        return redirect(url_for('not_logged'))
    if session['user_role'] != "Logistics Officer":
        error = "Only Logistics Officers have access to this page"
        return redirect(url_for('error', error=error))
    
    # POST method. 
    if request.method == 'POST':
        asset_tag  = request.form['asset_tag']
        source     = request.form['source']
        dest       = request.form['destination'] 
        req_date   = date.today() 

        if asset_tag == "":
            error = "asset tag cannot be blank"
            return redirect(url_for('error', error=error))

        search = """
                    SELECT a.asset_tag, f.facility_name 
                    FROM assets a
                    JOIN facilities f
                    ON a.asset_at = f.facility_pk
                    WHERE asset_tag = %s; 
                 """                                             # SQL search DB for asset tag. 
        cur.execute(search,(asset_tag,))                    
        res = cur.fetchone()

        if not res:                                              # No match, do nothing.
            error = "asset tag does not exist" 
            return redirect(url_for('error', error=error)) 
        if res[1] == "DISPOSED":                                 # Disposed already, do nothing. 
            error = "asset was disposed"
            return redirect(url_for('error', error=error))
        elif res[1] != source: 
            error = "asset is not at source facility specified"
            return redirect(url_for('error', error=error))
        else:
            create = """
                        INSERT INTO transfer_req (log_fk, asset_fk, source_fk, dest_fk, req_dt)
                        VALUES ( (SELECT user_pk FROM users WHERE username =%s) , 
                                 (SELECT asset_pk FROM assets WHERE asset_tag=%s), 
                                 (SELECT facility_pk FROM facilities WHERE facility_name = %s),
                                 (SELECT facility_pk FROM facilities WHERE facility_name = %s), 
                                  %s);
                     """                                                                     #SQL create transfe request.   
            cur.execute(create,(session['username'], asset_tag, source, dest, req_date,))
            conn.commit()
            return render_template('req_success.html') 

    # GET method. 
    search = """
                SELECT facility_name 
                FROM facilities; 
             """                                                      # SQL search for every facility in DB.
    cur.execute(search)
    res = cur.fetchall()

    facilities = []
    
    for row in res:
        if row[0] == 'DISPOSED':
            continue
        facilities.append(row[0]) 

    session['facilities'] = facilities                                # Used for select drop down menu in html.

    return render_template('transfer_req.html')

# approve_req page. 
@app.route('/approve_req', methods=('POST', 'GET',))
def approve_req():
    if session.get('logged_in') != True:                    # Must be logged in to visit this page. 
        return redirect(url_for('not_logged'))
    if session['user_role'] != "Facilities Officer":
        error = "Only Facilities Officers have access to this page"
        return redirect(url_for('error', error=error))
    
    # POST method. 
    if request.methods == 'POST':
        return


    # GET method. 
    return render_template('approve_req.html') 


# logout page.
@app.route('/logout')
def logout():
    session.clear()
    return render_template('logout.html')


# not_logged page.
@app.route('/not_logged')
def not_logged():
    return render_template('not_logged.html')


# error page.
@app.route('/error')
def error():
    return render_template('error.html', error=request.args.get('error'))


