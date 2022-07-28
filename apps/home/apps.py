from django.apps import AppConfig
import pandas as pd
import pickle as pk
import pandas as pd
import os

from sklearn import metrics

class PredictionConfig(AppConfig):
    name = 'apps.home'
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    CLASSIFIER_FOLDER = os.path.join(BASE_DIR, 'home/classifier/')
    MODEL_FILE = os.path.join(CLASSIFIER_FOLDER, "XGB_model.pickle")
    LABELENCODER_FILE = os.path.join(CLASSIFIER_FOLDER, "WD_label_encoder")
    METRICS_FILE = os.path.join(CLASSIFIER_FOLDER, "metrics.csv")

    with open(MODEL_FILE,'rb') as f:
        model = pk.load(f)
    with open(LABELENCODER_FILE, 'rb') as f:
        LabelEncoder = pk.load(f)
    metrics = pd.read_csv(METRICS_FILE,sep=';')