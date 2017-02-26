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
        if role == "":
            error = "roles caanot be empty" 
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
        e = dict()
        e['facility_name'] = row[0]
        e['facility_code'] = row[1]
        facility_table.append(e)

    session['facility_table'] = facility_table

    return render_template('add_facility.html') 


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


