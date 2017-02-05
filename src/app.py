# Web application for LOST database
# Creator: Luke Donnelly

from flask import Flask, render_template, request, url_for, redirect, session
import psycopg2


app = Flask(__name__)
app.secret_key = "A7/62%![1280TalA"

conn = psycopg2.connect(dbname='lost', host='127.0.0.1', port='5432')
cur = conn.cursor()


# login screen
@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['logged_in'] = True
        session['username'] = request.form['username']
        return redirect(url_for("filter"))

    return render_template('login.html')


# filter screen
@app.route('/filter', methods=['POST', 'GET'])
def filter():
    if session.get('logged_in') != True:
        return redirect(url_for('notlog'))

    if request.method == 'POST':
        if request.form['button'] == 'Inventory Report':
            session['facility'] = request.form['facility']
            session['date_f'] = request.form['date_f']
            return redirect(url_for("facility"))
        elif request.form['button'] == 'Transit Report':
            session['date_t'] = request.form['date_t']
            return redirect(url_for("transit"))
        elif request.form['button'] == 'Logout':
            return redirect(url_for("logout"))
        else:
            pass

    return render_template('filter.html')


# facility report screen
@app.route('/facility', methods=['POST', 'GET'])
def facility():
    if session.get('logged_in') != True:
        return redirect(url_for('notlog'))

    if request.method == 'POST':
        if request.form['button'] == 'Logout':
            return redirect(url_for("logout"))
        elif request.form['button'] == "Go Back":
            return redirect(url_for("filter"))
        else:
            pass

 # queries for options
 # --------------------------------------------------------------------------------
    SQL1 = """
            SELECT
                f.fcode,
                a.asset_tag,
                p.description As Product,
                at.arrive_dt,
                at.depart_dt
              FROM
                asset_at at
	                RIGHT OUTER JOIN assets a
	                    ON a.asset_pk=at.asset_fk
	                LEFT OUTER JOIN facilities f
	                    ON at.facility_fk = f.facility_pk
	                RIGHT OUTER JOIN products p
                        ON a.product_fk = p.product_pk
              WHERE
                fcode = %s;
           """

    SQL2 = """
                SELECT
                    f.fcode,
                    a.asset_tag,
                    p.description As Product,
                    at.arrive_dt,
                    at.depart_dt
                  FROM
                    asset_at at
    	                RIGHT OUTER JOIN assets a
    	                    ON a.asset_pk=at.asset_fk
    	                LEFT OUTER JOIN facilities f
    	                    ON at.facility_fk = f.facility_pk
    	                RIGHT OUTER JOIN products p
                            ON a.product_fk = p.product_pk
                  WHERE
                    at.arrive_dt = %s
               """

    SQL3= """
                 SELECT
                    f.fcode,
                    a.asset_tag,
                    p.description As Product,
                    at.arrive_dt,
                    at.depart_dt
                  FROM
                    asset_at at
    	                RIGHT OUTER JOIN assets a
    	                    ON a.asset_pk=at.asset_fk
    	                LEFT OUTER JOIN facilities f
    	                    ON at.facility_fk = f.facility_pk
    	                RIGHT OUTER JOIN products p
                            ON a.product_fk = p.product_pk
                  WHERE
                    fcode = %s AND at.arrive_dt = %s
               """
# --------------------------------------------------------------------------------------------
# end queries

    fcode = session['facility']
    date = session['date_f']

    # checks data fields
    if fcode != "" and date != "":  # Both fields are set
        data = (fcode, date,)
        SQL = SQL3
    elif date != "":                   # Date is just set
        data = (date,)
        SQL = SQL2
    else:                              # Default
        data = (fcode,)
        SQL = SQL1

    # tries the query, if fails go to logout screen
    try:
        cur.execute(SQL, data)
    except Exception:
        conn.rollback()
        return redirect(url_for('logout'))

    res = cur.fetchall()

    table = []
    for i in res:                # creates a dict for each row the query produces
        e = dict()
        e['fcode'] = i[0]
        e['asset'] = i[1]
        e['product'] = i[2]
        e['arrive'] = i[3]
        e['depart'] = i[4]
        table.append(e)

    session['table'] = table      # an array of dictionaries that html files use

    return render_template('facility.html')

# transit report screen
@app.route('/transit', methods=['POST', 'GET'])
def transit():
    if session.get('logged_in') != True:
        return redirect(url_for('notlog'))

    if request.method == 'POST':
        if request.form['button'] == 'Logout':
            return redirect(url_for("logout"))
        elif request.form['button'] == "Go Back":
            return redirect(url_for("filter"))
        else:
            pass

    SQL = """
            SELECT
                a.asset_tag,
                p.description,
                s.fcode,
                d.fcode,
                c.depart_dt,
                c.arrive_dt
            FROM
                assets a
                  LEFT OUTER JOIN asset_on ao
	                  ON ao.asset_fk = a.asset_pk
                  RIGHT OUTER JOIN products p
	                  ON a.product_fk = p.product_pk
                  RIGHT OUTER JOIN convoys c
	                  ON ao.convoy_fk = c.convoy_pk
                  RIGHT OUTER JOIN facilities s
	                  ON s.facility_pk = c.source_fk
                  RIGHT OUTER JOIN facilities d
	                  ON d.facility_pk = c.dest_fk

                  WHERE c.depart_dt = %s OR c.arrive_dt = %s
    """

    data = (session['date_t'], session['date_t'],)

    # tries the query, if fails go to logout screen
    try:
        cur.execute(SQL, data)
    except Exception:
        conn.rollback()
        return redirect(url_for('logout'))

    res = cur.fetchall()

    table = []
    for i in res:
        e = dict()                   # creates a dict for each row the query produces
        e['asset'] = i[0]
        e['product'] = i[1]
        e['source'] = i[2]
        e['dest'] = i[3]
        e['depart'] = i[4]
        e['arrive'] = i[5]
        table.append(e)              # an array of dictionaries that html files use

    session['table'] = table

    return render_template('transit.html')


# logout screen
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    if request.method == 'POST':
        if request.form['button'] == 'Go to Login Page':
            return redirect(url_for("login"))

    return render_template("logout.html")


# not logged in screen
@app.route('/not_logged', methods=['POST', 'GET'])
def notlog():
    if request.method == 'POST':
        if request.form['button'] == 'Login':
            return redirect(url_for("login"))

    return render_template('notlogged.html')

