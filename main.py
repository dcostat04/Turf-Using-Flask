import pymysql
from flask import Flask, flash,render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'TIGER'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'trevor@0409'
app.config['MYSQL_DB'] = 'pylogin'

mysql = MySQL(app)



@app.route('/', methods=['GET', 'POST'])
def login():
    msg = 'Please enter your usename and passwod'
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM account1 WHERE username = %s AND password = %s', (username, password,))
        acc = cursor.fetchone()
        if acc:
            session['loggedin'] = True
            session['id'] = acc['id']
            session['username'] = acc['username']
            return redirect(url_for('home'))
        else:
            msg = 'Incorrect username or password!'
    return render_template('index-1.html', msg=msg)

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
    return render_template('signup.html', msg=msg)

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

@app.route('/contact')
def contact():
    if 'loggedin' in session:
        return render_template("contact-us.html")
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run(debug=True);