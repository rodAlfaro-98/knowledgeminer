import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
import io
import sklearn
import urllib, base64
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler 

class PCAA():
	def __init__(self, dataset, paso1,paso2,paso34,paso5,paso6):
		self.dataset = dataset
		self.paso1 = paso1
		self.paso2 = paso2
		self.paso34 = paso34
		self.paso5 = paso5
		self.paso6 = paso6

	def get_correlacion(self):
		return self.paso1['correlacion']

	def get_estandarizacion(self):
		return self.paso2['estandarizacion']

	def get_matriz(self):
		return self.paso34['matriz']

	def get_proporcion(self):
		return self.paso5['proporcion']

	def get_acumulada(self):
		return self.paso5['acumulada']

	def get_grafica(self):
		return self.paso5['grafica']

	def get_cargasCom(self):
		return self.paso6['cargasCom']


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
	global Estand
	global MEstand

	Estand = StandardScaler()
	MEstand = Estand.fit_transform(dataset)
	df = pd.DataFrame(MEstand, columns=dataset.columns)
	paso2 = {
		'estandarizacion': df,
	}
	return paso2

def matrizCovCorr(dataset):
	global pca

	pca = PCA(0.85)
	pca.fit(MEstand)
	paso34 = {
		'matriz': pca.components_,
	}
	return paso34

def componentesPrincipales(dataset):
	pca.fit(MEstand)

	varianza = pca.explained_variance_ratio_
	paso5 = {
		'proporcion': varianza,
		'acumulada':varianza[0:6].sum(),
	}
	return paso5

def cargas(dataset):
	pca.fit(MEstand)

	CargasComponentes = pd.DataFrame(abs(pca.components_), columns=dataset.columns)
	paso6 = {
		'cargasCom': CargasComponentes,
	}
	return paso6

def initialization(file_path):
	dataset = pd.read_csv(file_path)
	dataset = dataset.iloc[0:500000]
	dataset = dataset.select_dtypes(include=['float64','int64'])
	paso1 = varCorrelacionadas(dataset)
	paso2 = estandarizacionDatos(dataset)
	paso34 = matrizCovCorr(dataset)
	paso5 = componentesPrincipales(dataset)
	paso6 = cargas(dataset)
	pca = PCAA(dataset,paso1,paso2,paso34,paso5,paso6)
	return pca
