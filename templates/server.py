from flask import Flask, flash, redirect, render_template, request, session, abort
 
app = Flask(__name__)
 
@app.route("/")
def index():
    return render_template(
    	'menu.html')
@app.route("/login/")
def inter():
    return render_template(
        'in.html')

@app.route("/registration/")
def registration():
    return render_template(
        'reg.html')

@app.route("/good/")
def interd():
    return render_template(
        'good.html')



 
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)