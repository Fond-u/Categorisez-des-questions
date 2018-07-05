from flask import Flask,render_template, jsonify, request


app = Flask(__name__) 

@app.route('/')
@app.route('/index/')
def index():
	return render_template('index.html') 