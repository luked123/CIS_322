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
                    SELECT u.username, r.role, u.active
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
            session['active']    = res[2]
            if session['active'] != True:
                session['logged_in'] = False                 # Logged in.
                return render_template('revoked.html')
            else: 
                session['logged_in'] = True
            return redirect(url_for('dashboard'))
    
    #GET method.
    return render_template('login.html') 


# dashboard page.
@app.route('/dashboard')
def dashboard():
    if session.get('logged_in') != True:                    # Must be logged in to visit this page. 
        return redirect(url_for('not_logged'))

    # GET method.
    if session['user_role'] == "Facilities Officer":  
        search = """
                    SELECT transfer_pk, req_dt
                    FROM transfer_req 
                    WHERE approved_bool IS UNKNOWN
                    ORDER BY req_dt asc; 
                  """                                        # SQL search for all transfer request that have not been checked
        cur.execute(search)
        res = cur.fetchall()

        work_table = [] 

        for row in res:
            e = dict()
            e['id'] = row[0]
            e['date'] = row[1]
            e['work_space'] = '/approve_req'
            work_table.append(e)
        
        session['work_type'] = "Transfer Requests"
        session['type_id']   = "Transfer Request ID"
        session['type_date']  = "Request Date" 
        session['work_table'] = work_table
    
    if session['user_role'] == "Logistics Officer":  
        search = """
                    SELECT ti.transfer_fk, tr.approve_dt
                    FROM transfer_info ti
                    JOIN transfer_req tr
                    ON tr.transfer_pk = ti.transfer_fk 
                    WHERE tr.approved_bool = 'true'  
                    ORDER BY tr.approve_dt asc; 
                  """                                        # SQL search for all transfer request that have been approved
        cur.execute(search)
        res = cur.fetchall()

        work_table = [] 

        for row in res:
            e = dict()
            e['id'] = row[0]
            e['date'] = row[1]
            e['work_space'] = '/update_transit' 
            work_table.append(e)

        session['work_type'] = "Transfer Update Schedule"
        session['type_id']   = "Transfer ID"
        session['type_date']  = "Approved Date" 
        session['work_table'] = work_table

    return render_template('dashboard.html')


# activate_user api.
@app.route('/activate_user', methods=('POST',))
def activate_user():
    # POST method. 
    if request.method=='POST' and 'arguments' in request.form:
        req = json.loads(request.form['arguments'])

        username = req['username']
        password = req['password']
        role     = req['role'] 
        dat = dict()

        search = """
                    SELECT role_pk FROM roles WHERE role = %s;
                 """                                                   # Check if role exists or not. 
        cur.execute(search,(role,))
        res = cur.fetchone()

        if not res:
            create = """
                        INSERT INTO roles (role) VALUES (%s); 
                     """
            cur.execute(create,(role,))                                 # Creates role if there isn't.
        

        search = """
                    SELECT username, active FROM users WHERE username = %s; 
                 """
        cur.execute(search,(username,))
        res = cur.fetchone();                                           # Search for username. 
        
        if not res:
            create = """
                        INSERT INTO users (username, password, role_fk, active)
                        VALUES (%s, %s, (SELECT role_pk FROM roles WHERE role = %s), 'true');
                     """
            cur.execute(create,(username,password,role,))
            dat['result'] = "Created user " + username + ", user is now active"          # Creates the user if doesn't exist 
        else:
            update = """
                        UPDATE users 
                        SET password = %s, active = 'true'
                        WHERE username = %s; 
                     """
            cur.execute(update,(password,username,))
            dat['result'] = "Activated user " + username                                #  Activates user and updates password
        
        conn.commit()

        data = json.dumps(dat)
        return data


#revoke_user api.
@app.route('/revoke_user', methods=('POST',))
def revoke_user():
    # POST method. 
    if request.method=='POST' and 'arguments' in request.form:
        req = json.loads(request.form['arguments'])

        username = req['username']                                          # Username to be revoked.
        dat = dict()

        search="""
                  SELECT username FROM users WHERE username = %s;         
               """                                                          # Search the database for username. 
        cur.execute(search,(username,))
        res = cur.fetchone()

        if not res:
            dat['result'] = "Username: " + username + " does not exist"     # User does not exist.
        else:
            update = """
                        UPDATE users
                        SET active = 'false'
                        WHERE username = %s
                     """
            cur.execute(update,(username,))                                  #  Revoke user and give confirmation. 
            dat['result'] = "Revoked user: " + username 

        conn.commit()
        
        data = json.dumps(dat)
        return data


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
                 """                                                           # SQL search DB for matching facility names.

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
                        INSERT INTO assets (asset_tag, asset_desc, initial_fk, initial_dt) 
                        VALUES (%s, %s, (SELECT facility_pk FROM facilities WHERE facility_name = %s), %s); 

                        INSERT INTO asset_at (asset_fk, facility_fk, arrival_dt, requested, transfering, transfered) 
                        VALUES ((SELECT asset_pk FROM assets WHERE asset_tag = %s),
                                (SELECT facility_pk FROM facilities WHERE facility_name = %s),
                                %s, 'false', 'false', 'false'); 
                    """                                                                                    # SQL create asset. 
            cur.execute(create,(asset_tag,asset_desc,facility_name,arrive_dt,asset_tag,facility_name,arrive_dt,))
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
        facilities.append(row[0]) 

    session['facilities'] = facilities                                 # Used for select drop down menu in html. 

    search = """
                SELECT asset_tag, asset_desc
                FROM assets; 
             """                                                       # SQL search for every asset in DB.
    cur.execute(search)
    res = cur.fetchall()
   
    asset_table = []

    for row in res:
        e = dict()
        e['asset_tag']  = row[0]
        e['asset_desc'] = row[1] 
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
                    SELECT a.asset_tag, dispose_dt
                    FROM assets a
                    WHERE asset_tag = %s; 
                 """                                             # SQL search DB for asset tag. 
        cur.execute(search,(asset_tag,))                    
        res = cur.fetchone()

        if not res:                                              # No match, do nothing.
            error = "asset tag does not exist" 
            return redirect(url_for('error', error=error)) 
        if res[1] != None:                                       # Disposed already, do nothing. 
            error = "asset was already disposed"
            return redirect(url_for('error', error=error)) 
        else:
            change = """
                        UPDATE assets
                        SET dispose_dt = %s 
                        WHERE asset_tag = %s; 
                     """                                         # SQL change asset to disposed. 
            cur.execute(change,(dispose_dt, asset_tag,))
            conn.commit()
            return redirect(url_for('dashboard')) 
    
    # GET method. 
    search = """
                SELECT asset_tag, asset_desc, dispose_dt
                FROM assets; 
             """                                                 # SQL search for every asset in DB.
    cur.execute(search)
    res = cur.fetchall()
   
    asset_table = []

    for row in res:
        if row[2] != None:
            continue
        e = dict()
        e['asset_tag']  = row[0]
        e['asset_desc'] = row[1] 
        asset_table.append(e)

    session['asset_table'] = asset_table
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
                        SELECT a.asset_tag, a.asset_desc, f.facility_code, at.arrival_dt, at.depart_dt, a.dispose_dt
                        FROM assets a 
                        JOIN asset_at at
                        ON at.asset_fk = a.asset_pk
                        JOIN facilities f
                        ON at.facility_fk = f.facility_pk
                        WHERE at.arrival_dt = %s OR at.depart_dt = %s OR a.dispose_dt = %s; 
                    """                                                 # SQL search assets matching date in all facilities.
            cur.execute(search,(date,date,date,))
            res = cur.fetchall() 
        
            asset_report_table = [] 

            for row in res: 
                e = dict()
                e['asset_tag']     = row[0]
                e['asset_desc']    = row[1]
                e['facility_code'] = row[2]
                e['arrival_dt']    = row[3]
                e['depart_dt']     = row[4] 
                e['dispose_dt']    = row[5]
                asset_report_table.append(e)

            session['asset_report_table'] =asset_report_table

            return render_template('asset_report.html')

        else:                                                       # Specific facility name. 
            search = """
                        SELECT a.asset_tag, a.asset_desc, f.facility_code, at.arrival_dt, at.depart_dt, a.dispose_dt
                        FROM assets a 
                        JOIN asset_at at
                        ON a.asset_pk = at.asset_fk
                        JOIN facilities f
                        ON at.facility_fk = f.facility_pk
                        WHERE f.facility_name = %s AND (at.arrival_dt = %s OR at.depart_dt = %s  OR a.dispose_dt = %s);
                    """                                              # SQL search assets in specific facility matching date. 
            cur.execute(search,(facility_name,date,date,date,))
            res = cur.fetchall() 

            asset_report_table = []

            for row in res: 
                e = dict()
                e['asset_tag']     = row[0]
                e['asset_desc']    = row[1]
                e['facility_code'] = row[2]
                e['arrival_dt']    = row[3]
                e['depart_dt']     = row[4] 
                e['dispose_dt']    = row[5]
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
        facilities.append(row[0]) 

    session['facilities'] = facilities                                 # Used for select drop down menu in html.

    return render_template('asset_report.html')


# transfer_report page. 
@app.route('/transfer_report')
def transfer_report():
    return render_template('transfer_report.html')


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
        req_date   = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

        if asset_tag == "":
            error = "asset tag cannot be blank"
            return redirect(url_for('error', error=error))

        search = """
                    SELECT a.asset_tag, a.dispose_dt, f.facility_name
                    FROM asset_at at
                    JOIN  facilities f
                    ON f.facility_pk = at.facility_fk
                    JOIN assets a
                    ON at.asset_fk = a.asset_pk
                    WHERE at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = %s) AND at.transfering = 'false' AND at.transfered = 'false' AND at.requested = 'false';  
                 """                                             # SQL search DB for asset tag. 
        cur.execute(search,(asset_tag,))                    
        res = cur.fetchone()

        if not res:                                              # No match, do nothing.
            error = "Asset tag does not exist OR transfer request for same asset needs to be approved/denied before making another request OR asset is in the process of having a transfer" 
            return redirect(url_for('error', error=error)) 
        if res[1] != None:                                       # Disposed already, do nothing. 
            error = "asset was disposed"
            return redirect(url_for('error', error=error))
        if res[2] != source:
            error = "asset is not located at source facility specified" 
            return redirect(url_for('error', error=error))
        else:
            create = """
                        INSERT INTO transfer_req (log_fk, asset_fk, source_fk, dest_fk, req_dt)
                        VALUES ( (SELECT user_pk FROM users WHERE username =%s) , 
                                 (SELECT asset_pk FROM assets WHERE asset_tag=%s), 
                                 (SELECT facility_pk FROM facilities WHERE facility_name = %s),
                                 (SELECT facility_pk FROM facilities WHERE facility_name = %s), 
                                  %s);

                        UPDATE asset_at 
                        SET requested = 'true'
                        WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag =%s) AND 
                                          transfering = 'false' AND transfered = 'false' AND requested = 'false';
                     """                                                                     #SQL create transfe request.   
            cur.execute(create,(session['username'], asset_tag, source, dest, req_date,asset_tag,))
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
        facilities.append(row[0]) 

    session['facilities'] = facilities                                # Used for select drop down menu in html.

    return render_template('transfer_req.html')

# update_transit page. 
@app.route('/update_transit', methods=('POST', 'GET'))
def update_transit(): 
    if session.get('logged_in') != True:                    # Must be logged in to visit this page. 
        return redirect(url_for('not_logged'))
    if session['user_role'] != "Logistics Officer":
        error = "Only Logistics Officers have access to this page"
        return redirect(url_for('error', error=error))
   
    # POST method.  
    if request.method == 'POST':
        load_dt   = request.form['load_dt'] 
        unload_dt = request.form['unload_dt']

        check = """
                    SELECT ti.unload_dt 
                    FROM transfer_info ti
                    WHERE ti.transfer_fk = %s; 
                """
        cur.execute(check, (session['transfer_id'],))
        res = cur.fetchone()

        if not res[0]:
            if not unload_dt:  
                update = """
                            UPDATE transfer_info 
                            SET load_dt = %s
                            WHERE transfer_fk = %s; 
                         """
                cur.execute(update, (load_dt, session['transfer_id'],))
                conn.commit()
            else:  
                update = """
                            UPDATE transfer_info 
                            SET load_dt = %s, unload_dt = %s
                            WHERE transfer_fk = %s; 

                            UPDATE asset_at
                            SET depart_dt = %s, transfered = 'true'
                            WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = %s) 
                            AND requested = 'true' AND transfering = 'true' AND transfered = 'false'; 

                            INSERT INTO asset_at (asset_fk, facility_fk, arrival_dt, requested, transfering, transfered)
                            VALUES ((SELECT asset_pk FROM assets WHERE asset_tag = %s), 
                                    %s,  %s, 'false', 'false', 'false'); 
                         """
                cur.execute(update, (load_dt, unload_dt, session['transfer_id'], load_dt, session['asset_tag'], session['asset_tag'], session['dest_fk'], unload_dt,))
                conn.commit()

            return redirect(url_for('dashboard'))
        else: 
            error = "Invalid request, unload time is already set"  
            return redirect(url_for('error', error=error))

    # GET method.     
    session['transfer_id'] = request.args['id'] 
    
    search = """
                SELECT ti.transfer_fk, a.asset_tag, ti.source_fk, ti.load_dt, ti.dest_fk, ti.unload_dt, u.username, tr.approve_dt
                FROM transfer_info ti
                JOIN assets a 
                ON asset_fk = asset_pk 
                JOIN transfer_req tr
                ON ti.transfer_fk = tr.transfer_pk
                JOIN users u
                ON tr.fac_fk = u.user_pk
                WHERE transfer_fk = %s; 
             """
    cur.execute(search, (session['transfer_id'],))
    res = cur.fetchone() 

    session['transfer_id'] = res[0]
    session['asset_tag']   = res[1]
    session['source_fk']   = res[2]
    session['load_dt']     = res[3]
    session['dest_fk']     = res[4]
    session['unload_dt']   = res[5]
    session['approved_by'] = res[6]
    session['approve_dt']  = res[7]

    search = """ 
                SELECT facility_code
                FROM facilities 
                WHERE facility_pk = %s; 
             """   
    cur.execute(search,(session['source_fk'],))
    res = cur.fetchone()

    session['source'] = res[0]

    search = """ 
                SELECT facility_code 
                FROM facilities 
                WHERE facility_pk = %s; 
             """   
    cur.execute(search,(session['dest_fk'],))
    res = cur.fetchone()

    session['dest'] = res[0] 

    return render_template('/update_transit.html') 

# approve_req page. 
@app.route('/approve_req', methods=('POST', 'GET',))
def approve_req():
    if session.get('logged_in') != True:                    # Must be logged in to visit this page. 
        return redirect(url_for('not_logged'))
    if session['user_role'] != "Facilities Officer":
        error = "Only Facilities Officers have access to this page"
        return redirect(url_for('error', error=error))
    
    # POST method. 
    if request.method == 'POST':
        button = request.form['button']
        approve_date   = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
      

        if button == "Approve":
            update = """
                        UPDATE transfer_req 
                        SET approved_bool = 'true', approve_dt = %s, fac_fk = (SELECT user_pk FROM users WHERE username = %s) 
                        WHERE transfer_pk = %s;

                        UPDATE asset_at
                        SET transfering = 'true' 
                        WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = %s) 
                        AND requested = 'true' AND transfering = 'false' AND transfered = 'false'; 
                     """
            cur.execute(update,(approve_date, session['username'], session['transfer_req'], session['asset_tag'],))
            null = None

            create = """
                        INSERT INTO transfer_info ( transfer_fk, asset_fk, source_fk, load_dt, unload_dt, dest_fk)
                        VALUES (%s,(SELECT asset_pk FROM assets WHERE asset_tag = %s), %s, %s, %s, %s); 
                     """
            cur.execute(create, (session['transfer_req'], session['asset_tag'],  session['source_fk'], null, null, session['dest_fk'],))
            conn.commit()

            return redirect(url_for('dashboard'))

        if button == "Reject": 
            update = """
                        UPDATE transfer_req
                        SET approved_bool = 'false' 
                        WHERE transfer_pk = %s;
                
                        UPDATE asset_at
                        SET requested = 'false' 
                        WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = %s) AND 
                        transfering = 'false' AND transfered = 'false' AND requested = 'true'; 
                      """
            cur.execute(update, (session['transfer_req'], session['asset_tag'],))
            conn.commit()

            return redirect(url_for('dashboard'))


    # GET method. 
    transfer_req = request.args['id']
    search = """
                SELECT tr.transfer_pk, u.username, a.asset_tag, tr.source_fk, tr.dest_fk, tr.req_dt
                FROM transfer_req tr
                JOIN users u 
                ON tr.log_fk = u.user_pk
                JOIN assets a 
                ON tr.asset_fk = a.asset_pk
                WHERE tr.transfer_pk = %s; 
             """
    cur.execute(search,(transfer_req,))
    res = cur.fetchone()

    session['transfer_req'] = res[0]
    session['requestor']    = res[1]
    session['asset_tag']    = res[2]
    session['source_fk']    = res[3]
    session['dest_fk']      = res[4]
    session['req_dt']       = res[5]

    search = """ 
                SELECT facility_code 
                FROM facilities 
                WHERE facility_pk = %s; 
             """   
    cur.execute(search,(session['source_fk'],))
    res = cur.fetchone()

    session['source'] = res[0]

    search = """ 
                SELECT facility_code 
                FROM facilities 
                WHERE facility_pk = %s; 
             """   
    cur.execute(search,(session['dest_fk'],))
    res = cur.fetchone()

    session['dest'] = res[0] 
   
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


