from flask import Flask, render_template, request, url_for, redirect, session

import psycopg2

app = Flask(__name__)
app.secret_key = "A7/62%![1280TalA"

conn = psycopg2.connect(dbname = 'lost', host='127.0.0.1', port='5432')
cur = conn.cursor()


@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for("welcome"))
    return render_template('login.html')


@app.route('/filter', methods=['POST', 'GET'])
def welcome():
    if request.method == 'POST':
        if request.form['button'] == 'Inventory Report':
            session['facility'] = request.form['facility']
            return redirect(url_for("facility"))
        elif request.form['button'] == 'Transit Report':
            session['date'] = request.form['date']
            return redirect(url_for("transit"))
        elif request.form['button'] == 'Logout':
            return redirect(url_for("logout"))
        else:
            pass
    return render_template('filter.html')


@app.route('/facility')
def facility():

    SQL = """
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

    data =(session['facility'],)
    cur.execute(SQL, data)
    res = cur.fetchall()

    table = []
    for i in res:
        e = dict()
        e['fcode'] = i[0]
        e['asset'] = i[1]
        e['product'] = i[2]
        e['arrive']  = i[3]
        e['depart']  = i[4]
        table.append(e)

    session['table'] = table

    return render_template('facility.html')


@app.route('/transit')
def transit():
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

    data = (session['date'],session['date'],)
    cur.execute(SQL, data)
    res = cur.fetchall()

    table = []
    for i in res:
        e = dict()
        e['asset'] = i[0]
        e['product'] = i[1]
        e['source'] = i[2]
        e['dest'] = i[3]
        e['depart'] = i[4]
        e['arrive'] =i[5]
        table.append(e)

    session['table'] = table

    return render_template('transit.html')


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    if request.method == 'POST':
        if request.form['button'] == 'Go to Login Page':
            return redirect(url_for("login"))
    return render_template("logout.html")


if __name__ == '__main__':
    app.run(debug=True)
