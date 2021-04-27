import pymysql
from flask import Flask, flash,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'TIGER'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'trevor@0409'
app.config['MYSQL_DB'] = 'temp'

mysql = MySQL(app)



@app.route('/', methods=['GET', 'POST'])
def login():
    msg = 'Please enter your usename and passwod'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account1 WHERE username = %s AND passw = %s', (username, password,))
        acc = cursor.fetchone()
        if acc:
            session['loggedin'] = True
            session['id'] = acc['id']
            session['username'] = acc['username']
            session['phone']=acc['phone']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username or password!'
    return render_template('login1.html', msg=msg)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = 'Sign up!'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'phone' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account1 WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'[0-9]+', phone):
            msg = 'phone no must contain only  numbers!'
        elif not username or not password or not email or not phone:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO account1 VALUES (NULL, %s, %s, %s,%s)', (username, password, email,phone,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('registration.html', msg=msg)

@app.route('/owner/login', methods=['GET', 'POST'])
def admlogin():
    msg = 'Please enter your username and password'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account2 WHERE username = %s AND password = %s', (username, password,))
        acc2 = cursor.fetchone()
        if acc2:
            session['loggedin'] = True
            session['username'] = acc2['username']
            return redirect(url_for('admhome'))
        else:
            msg = 'Incorrect username or password!'
    return render_template('login2.html', msg=msg)

@app.route('/owner/logout')
def admlogout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('admlogin'))

@app.route('/owner/register', methods=['GET', 'POST'])
def admregister():
    msg = 'Sign up!'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'phone' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account2 WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'[0-9]+', phone):
            msg = 'phone no must contain only  numbers!'
        elif not username or not password or not email or not phone:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO account2 VALUES (NULL, %s, %s, %s,%s)', (username, password, email,phone,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('regown.html', msg=msg)

@app.route('/owner/home')
def admhome():
    if 'loggedin' in session:
        if 'loggedin' in session:
            username = session['username']

            cursor = mysql.connection.cursor()
            cursor.execute("select customer_name, cust_phone,b_date,starttime ,endtime  from bookings where turf_name=%s", (username,))
            mb = cursor.fetchall()
            print(mb)
            return render_template("indexown.html", username=session['username'],value=mb)
    return redirect(url_for('admlogin'))
@app.route('/home')
def home():
    if 'loggedin' in session:
        return render_template("index.html", username=session['username'])
    return redirect(url_for('login'))

@app.route('/turfs')
def turfs():
    if 'loggedin' in session:
        return render_template("turf.html", username=session['username'])
    return redirect(url_for('login'))


@app.route('/chemburturfs')
def chembur():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select distinct(t_date) t_date from location inner join turf on lid=ltid inner join dates on tid=tdid where l_name='chembur' and t_name ='ACRES CLUB' and sta is null")
        vt1 = cursor.fetchall()
        # print(vt1)
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select distinct(t_date) t_date from location inner join turf on lid=ltid inner join dates on tid=tdid where l_name='chembur' and t_name ='CHEMBUR KARNATAKA' and sta is null")
        vt2 = cursor.fetchall()

        return render_template("chembur.html", username=session['username'], vat1=vt1, vat2=vt2)
    return redirect(url_for('login'))


@app.route('/thaneturfs')
def thane():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select distinct(t_date) t_date from location inner join turf on lid=ltid inner join dates on tid=tdid where l_name='thane' and t_name ='URBAN SPORTS' and sta is null")
        vt1 = cursor.fetchall()
        # print(vt1)
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select distinct(t_date) t_date from location inner join turf on lid=ltid inner join dates on tid=tdid where l_name='thane' and t_name ='BOUNCE FOOTBALL' and sta is null")
        vt2 = cursor.fetchall()

        return render_template("thane.html", username=session['username'], vat1=vt1, vat2=vt2)
    return redirect(url_for('login'))


@app.route('/vashiturfs')
def vashi():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select distinct(t_date) t_date from location inner join turf on lid=ltid inner join dates on tid=tdid where l_name='vashi' and t_name ='NMSA' and sta is null")
        vt1 = cursor.fetchall()
        # print(vt1)
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select distinct(t_date) t_date from location inner join turf on lid=ltid inner join dates on tid=tdid where l_name='vashi' and t_name ='GOALBOX SAINATH' and sta is null")
        vt2 = cursor.fetchall()

        return render_template("vashi.html", username=session['username'], vat1=vt1, vat2=vt2)
    return redirect(url_for('login'))


@app.route('/booking')
def booking():
    if 'loggedin' in session:
        username = session['username']
        cursor = mysql.connection.cursor()
        cursor.execute("select * from bookings where customer_name=%s", (username,))
        mb = cursor.fetchall()
        print(mb)
        return render_template("booking.html", value=mb)
    return redirect(url_for('login'))


@app.route("/slot", methods=['GET', 'POST'])
def slot():
    # print(request.form)
    if request.method == 'POST' and 't_date' in request.form and 't_name' in request.form and 'l_name' in request.form:
        date = request.form['t_date']
        turf = request.form['t_name']
        locat = request.form['l_name']
        # print(date,turf,locat)
        cursor = mysql.connection.cursor()
        cursor.execute(
            "select start_time,end_time,sta from location inner join turf on lid=ltid inner join dates on tid=tdid where l_name=%s and t_name =%s and t_date=%s and sta is null order by start_time ASC  ",
            (locat, turf, date,))
        dts = cursor.fetchall()
        # print(dts)
        return render_template('slot.html', valueS=dts, l=locat, t=turf, d=date)
    return redirect(url_for('login'))


@app.route("/booknow", methods=['GET', 'POST'])
def booknow():
    if 'loggedin' in session:
        username = session['username']
        phone = session['phone']
        # print(request.form)
        if request.method == 'POST' and 'b_date' in request.form and 'slot' in request.form and 'turf_name' in request.form and 'locat' in request.form:
            date = request.form['b_date']
            turf = request.form['turf_name']
            locat = request.form['locat']
            slot = request.form['slot']
            # print(slot)
            Dict = eval(slot)
            starttime = Dict["st"]
            endtime = Dict["et"]
            # print(starttime,endtime)
            # st=slot[1]
            # print(date,turf,locat,slot,endtime)
            cursor = mysql.connection.cursor()
            cursor.execute(
                "insert into bookings(customer_name,cust_phone,locat,turf_name,b_date,starttime,endtime) values(%s,%s,%s,%s,%s,%s,%s)",
                (username, phone, locat, turf, date, starttime, endtime,))
            mysql.connection.commit()
            cursor.execute(
                "update dates inner join turf on tid=tdid inner join location on lid=ltid set sta='booked' where l_name=%s and t_name=%s and t_date=%s and start_time=%s",
                (locat, turf, date, starttime))
            mysql.connection.commit()
            # print(booked)
            return redirect(url_for('booking'))
        return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True);