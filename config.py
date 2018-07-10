import os

# Database initialization
basedir = os.path.abspath(os.path.dirname(__file__))
datadir = os.path.join(basedir,"tagapp", "data")
EX = os.path.join(datadir, 'exemple_quest.pkl')
MODEL = os.path.join(datadir, 'model_gs.pkl')
VECTO = os.path.join(datadir, 'vectoriser.pkl')
VECTOIDF = os.path.join(datadir, 'vectoriser_idf.pkl')
MODELSUP = os.path.join(datadir, 'model_sup.pkl')
MLB  = os.path.join(datadir, 'multilabelbinarizer.pkl')