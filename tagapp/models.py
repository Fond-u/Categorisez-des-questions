import numpy as np
import pandas as pd
from sklearn.externals import joblib
from bs4 import BeautifulSoup
import nltk

class OneQuestion:
	def __init__(self, df):
		self.data = df

	def get_data(self):
		return self.data

	def get_question(self):
		question = self.data.Body
		return BeautifulSoup(question, "html.parser").get_text()

	def get_titre(self):
		titre = self.data.Title
		return titre

	def get_tag(self):
		tag = self.data.Tags
		return nltk.RegexpTokenizer(r'[a-zA-Z0-9.#_+-]+').tokenize(tag)
 
class SetOfQuestions:
	def __init__(self, file_location):
		self.data = joblib.load(file_location) 

	def test(self):
		return self.data.shape

	def select_random_question(self):
		id_quest = self.element_aleat()
		self.one = OneQuestion(self.data.iloc[id_quest])
		return id_quest

	def select_question(self,id_quest):
		data_one = self.data.iloc[id_quest]
		self.one = OneQuestion(self.data.iloc[id_quest])
		return id_quest

	def selected_data(self):
		return self.one

	def selected_titre(self):
		return self.one.get_titre()

	def selected_question(self):
		return self.one.get_question()

	def selected_tag(self):
		return self.one.get_tag()

	def element_aleat(self):
		return  np.random.randint(0, self.data.shape[0], 1)[0]

class LDA:
	"""docstring for ClassName"""
	def __init__(self, model_loc, vecto_loc):
		"""initialisation"""
		self.data = joblib.load(model_loc) 
		self.model = self.data.best_estimator_
		self.vectoriser = joblib.load(vecto_loc) 
	
	def show_topics(self, n_words = 5):
		"""retourne les premier mot de chaques topics"""
		keywords = np.array(self.vectoriser.get_feature_names())
		topic_keywords = []
		for topic_weights in self.model.components_:
			top_keyword_locs = (-topic_weights).argsort()[:n_words]
			opic_keywords.append(keywords.take(top_keyword_locs))
		return topic_keywords

	def show_topics_and_coef(self, n_words = 5):
		keywords = np.array(self.vectoriser.get_feature_names())
		topic_keywords = []
		for topic_weights in self.model.components_:
			top_keyword_locs = (-topic_weights).argsort()[:n_words]
			tup = keywords.take(top_keyword_locs),topic_weights.take(top_keyword_locs)
			tup = [(keywords.take(loc),int(topic_weights.take(loc))) for loc in top_keyword_locs]
			topic_keywords.append((tup))
		return topic_keywords

	def predict_topic(self, corpus, n_top):
		df_topic_keywords_coef = pd.DataFrame(self.show_topics_and_coef(n_top))
		X = self.vectoriser.transform(corpus)
		topic_scores = self.model.transform(X)
		mots_coef = [] 
		for itx,row in enumerate(df_topic_keywords_coef.iterrows()):
			for tup in row[1]:
				mots_coef.append((tup[0],tup[1]*topic_scores[0][itx]))
				
		mots_coef_sorted = sorted(mots_coef, key=(lambda item: item[1]), reverse=True)
		mots, coef =  zip(*mots_coef_sorted)
		return(mots[:n_top])

class LR:
	"""docstring for ClassName"""
	def __init__(self, model_loc, vecto_loc, mlb_loc):
		self.model = joblib.load(model_loc) 
		self.vectoriser = joblib.load(vecto_loc) 
		self.multilabeliser = joblib.load(mlb_loc) 

	def predidction(self, corpus, n):
		probs_min = []
		X = self.vectoriser.transform(corpus)
		proba = self.model.predict_proba(X)
		for prob in proba: 
			probs_min.append(-1*prob[0][1])
		arg_order = np.array(probs_min).argsort()[:n]
		return self.multilabeliser.classes_[arg_order]
		