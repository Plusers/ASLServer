from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///tutorial.db', echo=True)

 
app = Flask(__name__)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello !  <a href='/logout'>Logout</a>"
@app.route('/test')
def test():
 
    POST_USERNAME = "python"
    POST_PASSWORD = "python"
    POST_SEC_PASSWORD = "python"
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.login.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]),User.sec_password.in_([POST_SEC_PASSWORD]) )
    result = query.first()
    if result:
        return "Object found"
    else:
        return "Object not found " + POST_USERNAME + " " + POST_PASSWORD + " " + POST_SEC_PASSWORD
@app.route('/login', methods=['POST'])

def do_admin_login():
    if POST_USERNAME==request.form['username'] and POST_PASSWORD == request.form['password']:
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
    POST_USERNAME = str(request.form['login'])
    POST_PASSWORD = str(request.form['password'])
    POST_SEC_PASSWORD = str(request.form['sec_password'])

 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.login.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]),User.sec_password.in_([POST_SEC_PASSWORD]) )
    result = query.first()
    if len(request.form['password']) >= 8 and result and  request.form['login'] != "" and len(request.form['sec_password']) >= 8 and request.form['password'] == request.form['sec_password']:
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