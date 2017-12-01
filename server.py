from flask import Flask, flash, redirect, render_template, request, session, abort
 
app = Flask(__name__)
 
@app.route("/")
def index():
    return "Flask App!"
 
@app.route("/hello")
def hello():
    return "Hello"

@app.route("/in")
def inter():
    return render_template("in.html")

@app.route("/login")
def reg():
    return render_template("reg.html")
 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
