import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
from sklearn.ensemble import RandomForestClassifier
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import io
import urllib, base64

class BA():
    def __init__(self,X_train, X_validation, Y_train, Y_validation,dataset,dependiente,X):
        self.X_train = X_train
        self.X_validation = X_validation
        self.Y_train = Y_train
        self.Y_validation = Y_validation
        self.arbol = RandomForestClassifier(random_state = 0)
        self.dataset = dataset
        self.dependiente = dependiente
        self.X = X
        self.dataset = dataset

    def train(self):
        return self.arbol.fit(self.X_train, self.Y_train.ravel())

    def predict(self):
        self.Y_ClasificacionBA = self.arbol.predict(self.X_validation)
        return self.Y_ClasificacionBA
        
    def get_accuracy(self):
        return accuracy_score(self.Y_validation, self.Y_ClasificacionBA)

    def get_matriz_clasificacion(self):
        return pd.crosstab(self.Y_validation.ravel(), self.Y_ClasificacionBA, rownames=['Reales'], colnames=['Classificación'])

    def get_reporte_clasificacion(self):
        words = [i.split(' ') for i in classification_report(self.Y_validation, self.Y_ClasificacionBA).replace('macro avg','macro_avg').replace('weighted avg','weighted_avg').split('\n')]
        return [self.arbol.criterion, self.arbol.feature_importances_, self.get_accuracy(),classification_report(self.Y_validation, self.Y_ClasificacionBA)]
    
    def get_var_graphs(self):
        plt.clf()
        numtype = self.dataset.describe(include=['float64','int64']).columns
        c = self.dataset[self.dependiente]
        if self.dependiente not in numtype:
            c = [ i for i in range(len(c.tolist()))]
        plt.scatter(self.dataset[numtype[2]], self.dataset[numtype[1]], c = c)
        plt.grid()
        plt.xlabel(numtype[2])
        plt.ylabel(numtype[1])
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        buf.truncate(0)
        return uri
    
    def get_indep_vars(self):
        return [self.X,self.dataset[self.X]]
    
    def get_dep_vars(self):
        return [self.dependiente,self.dataset[self.dependiente]]
    
    def get_size_division(self):
        return [len(self.X_train),len(self.X_validation)]

    def get_corr_graph(self):
        plt.clf()
        MatrizInf = np.triu(self.dataset.corr())
        sns.heatmap(self.dataset.corr(), cmap='RdBu_r', annot=True, mask=MatrizInf)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        buf.truncate(0)
        return uri

    def get_comparation(self):
        return pd.DataFrame(self.Y_validation,self.predict())
    
    def get_bosque(self):
        return self.arbol
    
    def get_X_validation(self):
        return self.X_validation
    
    def get_Y_validation(self):
        return self.Y_validation
    
    def get_train(self):
        return [self.X_train, self.Y_train.ravel()]

def separacion(dataset,dependiente):
    y = np.array(dataset[[dependiente]])
    columnas = dataset.select_dtypes(include=['float64','int64']).columns.tolist()
    if dependiente in columnas:
        columnas.remove(dependiente)
    x = np.array(dataset[columnas])
    return [x,y,columnas]

def train_validation(x,y):
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(x, y, 
                                                                                test_size = 0.2, 
                                                                                random_state = 0,
                                                                                shuffle = True)
    return [X_train, X_validation, Y_train, Y_validation]

def initialization(file_path,dependiente):
    dataset = pd.read_csv(file_path)
    dataset = dataset.iloc[0:500000]
    x,y,columnas = separacion(dataset,dependiente)
    X_train, X_validation, Y_train, Y_validation = train_validation(x,y)
    return BA(X_train, X_validation, Y_train, Y_validation,dataset,dependiente,columnas)
