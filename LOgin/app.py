from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
 
app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello !  <a href='/logout'>Logout</a>"
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    
    
    if request.form['password'] == '123' and request.form['username'] == "admin":
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/reg')
def home_1():
    if not session.get('reg_in'):
        return render_template('reg.html')
    else:
        return "Hello !  <a href='/good'>Logout</a>"
 
@app.route('/reg_login', methods=['POST'])
def do_admin_login_1():
    if len(request.form['password']) >= 8 and request.form['login'] != "":
        session['reg_in'] = True
    else:
        flash('wrong password!')
    return home_1()

@app.route("/good")
def good():
    session['reg_in'] = False
    return home_1()

    


 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)