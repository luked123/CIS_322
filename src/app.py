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

        if not res:                                          # if response is an empty list, insert username/password pair   
            create = """
                        INSERT INTO users (username, password) 
                        VALUES ( %s, %s);
                     """                                     # SQL query
            cur.execute(create,(username, password,))
            conn.commit()
            return render_template('added.html')

        else:                                                     
            error = "username already exists"
            return redirect(url_for('error', error=error))    

        return  username

    return render_template('create_user.html')


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


