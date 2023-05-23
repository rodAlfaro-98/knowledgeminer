import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
import io
import sklearn
import urllib, base64
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler 

class PCA():
	def __init__(self, dataset, paso1,paso2):
		self.dataset = dataset
		self.paso1 = paso1
		self.paso2 = paso2
		#self.paso34 = paso34
		#self.paso5 = paso5
		#self.paso6 = paso6

	def get_correlacion(self):
		return self.paso1['correlacion']

	def get_estandarizacion(self):
		return self.paso2['estandarizacion']


def varCorrelacionadas(dataset):
	plt.figure(figsize=(14,7))
	corr = dataset.corr(method='pearson')
	Matriz = np.triu(corr)
	sns.heatmap(corr, cmap='RdBu_r', annot=True, mask=Matriz)
	buf = io.BytesIO()
	plt.savefig(buf,format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())
	uri = urllib.parse.quote(string)
	
	paso1 = {
		'correlacion': uri,
	}
	return paso1

def estandarizacionDatos(dataset):
	Estand = StandardScaler()
	MEstand = Estand.fit_transform(dataset)
	df = pd.DataFrame(MEstand, columns=dataset.columns)
	paso2 = {
		'estandarizacion': df,
	}
	return paso2

def initialization(file_path):
	dataset = pd.read_csv(file_path)
	paso1 = varCorrelacionadas(dataset)
	paso2 = estandarizacionDatos(dataset)
	pca = PCA(dataset,paso1,paso2)
	return pca		