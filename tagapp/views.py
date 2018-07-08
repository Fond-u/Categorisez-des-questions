from flask import Flask,render_template, jsonify, request
from .utils import *
from .models import *

app = Flask(__name__) 
app.config.from_object('config')

soq = SetOfQuestions(app.config['EX'])

@app.route('/')
@app.route('/index/', methods=['GET', 'POST'])
def index():

	if request.method == 'POST':
		action = request.form['action']
		if action == 'remplir':
			soq.select_question()
			titre = soq.selected_titre()
			corp = soq.selected_question()
			tag = soq.selected_tag()
			tag_lda = []
			tag_rl = []
		elif action == 'Valider':
			titre = request.form['tit']
			corp = request.form['corp']
			tag = []
			tag_lda = []
			tag_rl = []
		else:
			corp = ""
			titre = ""
			tag = []
			tag_lda = []
			tag_rl = []
		print('post')

	else:
		action = ""
		corp = ""
		titre = ""
		tag = []
		tag_lda = []
		tag_rl = []
		print('pas post')

	return render_template('index.html', val_titre=titre , val_corp=corp, val_tag_true=tag,
							val_tag_lda = tag_lda, val_tag_rl = tag_rl) 