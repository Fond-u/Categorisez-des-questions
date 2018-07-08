import numpy as np
from sklearn.externals import joblib
from bs4 import BeautifulSoup
import nltk

class OneQuestion:
	def __init__(self, titre, question, tag):
		self.titre = titre
		self.question = question
		self.tag = tag

	def get_question(self):
		return BeautifulSoup(self.question, "html.parser").get_text()

	def get_titre(self):
		return self.titre

	def get_tag(self):
		return nltk.RegexpTokenizer(r'[a-zA-Z0-9.#_+-]+').tokenize(self.tag)
 
class SetOfQuestions:
	def __init__(self, file_location):
		self.data = joblib.load(file_location) 

	def test(self):
		return self.data.shape

	def select_question(self):
		data_one = self.data.iloc[self.element_aleat()]
		self.one = OneQuestion(data_one.Title, data_one.Body, data_one.Tags)

	def selected_titre(self):
		return self.one.get_titre()

	def selected_question(self):
		return self.one.get_question()

	def selected_tag(self):
		return self.one.get_tag()

	def element_aleat(self):
		return  np.random.randint(0, self.data.shape[0], 1)[0]

