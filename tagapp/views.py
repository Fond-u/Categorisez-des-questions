from flask import Flask,render_template, jsonify, request
import nltk
from .utils import *
from .models import *

app = Flask(__name__) 
app.config.from_object('config')

soq = SetOfQuestions(app.config['EX'])
nltk.download('popular')

@app.route('/')
@app.route('/index/', methods=['GET', 'POST'])
def index():

	if request.method == 'POST':
		action = request.form['action']
		if action == 'remplir':
			exemple = soq.select_random_question()
			titre = soq.selected_titre()
			corp = soq.selected_question()
			tag = soq.selected_tag()
			tag_lda = []
			tag_rl = []
			corpus = ""
			voir_corpus = 0
		elif action == 'Valider':
			exemple = soq.select_question(int(request.form['id_ex']))
			titre = request.form['tit']
			corp = request.form['corp']
			corpus = build_corpus_element(titre, corp)
			lda_model = LDA(app.config['MODEL'], app.config['VECTO'])
			tag_lda = lda_model.predict_topic(corpus = [corpus], n_top = 5)
			rl_model  = LR(app.config['MODELSUP'], app.config['VECTOIDF'], app.config['MLB'])
			tag_rl = rl_model.predidction([corpus], 5)
			voir_corpus = 0
			
			if corpus == build_corpus_data(soq.selected_data().get_data()):
				tag = soq.selected_tag()
			else:
				tag = []
				
			if (titre + corp) == "":
				action = ""
				tag = []
				tag_lda = []
				tag_rl = []
				corpus = ""
		elif action == 'Corpus':
			exemple = soq.select_question(int(request.form['id_ex']))
			titre = request.form['tit']
			corp = request.form['corp']
			corpus = build_corpus_element(titre, corp)
			if corpus == build_corpus_data(soq.selected_data().get_data()):
				tag = soq.selected_tag()
			else:
				tag = []
			tag_lda = nltk.RegexpTokenizer(r'[a-zA-Z0-9.#_+-]+').tokenize(request.form['val_tag_lda'])
			tag_rl = []
			
			voir_corpus = 1
		else:
			exemple = 0
			corp = ""
			titre = ""
			tag = []
			tag_lda = []
			tag_rl = []
			corpus = ""
			voir_corpus = 0

	else:
		action = ""
		exemple = 0
		corp = ""
		titre = ""
		tag = []
		tag_lda = []
		tag_rl = []
		corpus = ""
		voir_corpus = 0


	return render_template('index.html', val_titre=titre , val_corp=corp, val_tag_true=tag,
							val_tag_lda = tag_lda, val_tag_rl = tag_rl, id_ex = exemple, last_act = action,
							corpus = corpus, voir_corpus = voir_corpus) 