import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
import io
import urllib, base64
import sklearn
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.tree import export_text

class AD():
	def __init__(self,dataset,paso1,paso2,paso3,paso4,paso5,paso6,paso7):
		self.dataset = dataset
		self.paso1 = paso1
		self.paso2 = paso2
		self.paso3 = paso3
		self.paso4 = paso4
		self.paso5 = paso5
		self.paso6 = paso6
		self.paso7 = paso7
		self.new_registro = False

	def add_new_registro(self):
		self.new_registro = True
	
	def is_new_registro(self):
		return self.new_registro
	
	def set_new_data(self,data):
		self.new_data = data
	
	def predict_new(self):
		return self.paso5['arbol'].predict(self.new_data)
	
	def get_new_data(self):
		return self.new_data

	def get_datos(self):
		return self.paso1['datos']

	def get_datos1(self):
		return self.paso1['datos1']

	def get_datos2(self):
		return self.paso1['datos2']

	def get_selCar(self):
		return self.paso2['selCar']

	def get_varPred(self):
		return self.paso3['varPred']

	def get_varClas(self):
		return self.paso3['varClas']

	def get_xTrain(self):
		return self.paso4['xTrain']

	def get_xVal(self):
		return self.paso4['xVal']

	def get_clasif(self):
		return self.paso5['clasif']

	def get_yclasif(self):
		return self.paso5['yclasif']

	def get_valM(self):
		return self.paso5['valM']

	def get_resultado(self):
		return self.paso5['resultado']

	def get_mClasif(self):
		return self.paso6['mClasif']

	def get_criterio(self):
		return self.paso6['criterio']

	def get_impVar(self):
		return self.paso6['impVar']

	def get_exactitud(self):
		return self.paso6['exactitud']

	def get_reporte(self):
		return self.paso6['reporte']

	def get_impMod(self):
		return self.paso7['impMod']

	def get_arbol_graph(self):
		return self.paso7['arbol']

	def get_rep(self):
		return self.paso7['rep']

	def get_accuracy(self):
		return self.paso5['resultado']

	def get_arbol(self):
		return self.paso5['arbol']
	
	def get_X_validation(self):
		return X_validation
	
	def get_Y_validation(self):
		return Y_validation
	
	def get_columnas(self):
		return self.paso7['columnas']

def accesoDatos(dataset,dependiente):
	dat = dataset.groupby(dependiente).size()
	paso1 = {
		'datos': dataset.dtypes,
		'datos1': dat,
		'datos2': dataset.describe(),
	}
	return paso1

def selCaracteristcas(dataset):
	plt.clf()
	MatrizInf = np.triu(dataset.corr())
	sns.heatmap(dataset.corr(), cmap='RdBu_r', annot=True, mask=MatrizInf)
	buf = io.BytesIO()
	plt.savefig(buf, format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())
	uri = urllib.parse.quote(string)
	buf.truncate(0)
	paso2 = {
		'selCar': uri,
	}
	return paso2

def definicionVar(dataset,dependiente):
	global X 
	global Y
	
	columnas = dataset.select_dtypes(include=['float64','int64']).columns.tolist()
	if(dependiente in columnas):
		columnas.remove(dependiente)
	X = np.array(dataset[columnas])
	superX = pd.DataFrame(X)

	Y = np.array(dataset[[dependiente]])
	superY = pd.DataFrame(Y)
	paso3 = {
		'varPred': superX,
		'varClas': superY,
	}
	return paso3

def creacionMod(dataset):
	global X_train
	global X_validation
	global Y_train
	global Y_validation

	X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, 
                                                                                test_size = 0.2, 
                                                                                random_state = 0,
                                                                                shuffle = True)
	paso4 = {
		'xTrain': len(X_train),
		'xVal': len(X_validation,)
	}
	return paso4

def modeloAd(dataset,max_depth,min_samples_split,min_samples_leaf):
	global ClasificacionAD
	global Y_ClasificacionAD

	#Se entrena el modelo a partir de los datos de entrada
	#ClasificacionAD = DecisionTreeClassifier(random_state=0)
	#ClasificacionAD.fit(X_train, Y_train)
	ClasificacionAD = DecisionTreeClassifier(max_depth=max_depth, 
                                         min_samples_split=min_samples_split, 
                                         min_samples_leaf=min_samples_leaf,
                                         random_state=0)
	z = ClasificacionAD.fit(X_train, Y_train)

	Y_ClasificacionAD = ClasificacionAD.predict(X_validation)

	ValoresMod1 = pd.DataFrame(Y_validation, Y_ClasificacionAD)
	paso5 = {
		'arbol': ClasificacionAD,
		'clasif': z,
		'yclasif': Y_ClasificacionAD,
		'valM': ValoresMod1,
		'resultado': accuracy_score(Y_validation, Y_ClasificacionAD),
	}
	return paso5

def matrizClasificacion(dataset):
	ModeloClasificacion1 = ClasificacionAD.predict(X_validation)
	Matriz_Clasificacion1 = pd.crosstab(Y_validation.ravel(), 
                                   ModeloClasificacion1, 
                                   rownames=['Reales'], 
                                   colnames=['Clasificación'])

	paso6 = {
		'mClasif': Matriz_Clasificacion1,
		'criterio': ClasificacionAD.criterion,
		'impVar': ClasificacionAD.feature_importances_,
		'exactitud': accuracy_score(Y_validation, Y_ClasificacionAD),
		'reporte': classification_report(Y_validation, Y_ClasificacionAD),
	}
	return paso6

def eficonfMod(dataset,dependiente):
	columnas = dataset.select_dtypes(include=['float64','int64']).columns.tolist()
	if dependiente in columnas:
		columnas.remove(dependiente)
	ImportanciaMod1 = pd.DataFrame({'Variable': list(dataset[columnas]),
                                'Importancia': ClasificacionAD.feature_importances_}).sort_values('Importancia', ascending=False)

	plt.figure(figsize=(16,16))
	plt.title('Arbol de decisión generado')
	plot_tree(ClasificacionAD, feature_names = columnas)
	buf1 = io.BytesIO()
	plt.savefig(buf1,format='png')
	buf1.seek(0)
	string = base64.b64encode(buf1.read())
	uri1 = urllib.parse.quote(string)

	Reporte = export_text(ClasificacionAD, feature_names = columnas)

	paso7 ={
		'impMod': ImportanciaMod1,
		'arbol': uri1,
		'rep': Reporte,
		'columnas': columnas
	}
	return paso7

def initialization(file_path,dependiente,request):
	dataset = pd.read_csv(file_path)
	dataset = dataset.iloc[0:500000]
	paso1 = accesoDatos(dataset,dependiente)
	paso2 = selCaracteristcas(dataset)
	paso3 = definicionVar(dataset,dependiente)
	paso4 = creacionMod(dataset)
	max_depth = None
	min_samples_leaf = 1
	min_samples_split = 2
	if 'csrfmiddlewaretoken' in request.GET:
		max_depth = int(request.GET['max_depth']) if int(request.GET['max_depth']) > 0 else None
		min_samples_split = int(request.GET['min_samples_split']) if int(request.GET['min_samples_split']) > 2 else 2
		min_samples_leaf = int(request.GET['min_samples_leaf']) if int(request.GET['min_samples_leaf']) > 1 else 1
	paso5 = modeloAd(dataset,max_depth,min_samples_split,min_samples_leaf)
	paso6 = matrizClasificacion(dataset)
	paso7 = eficonfMod(dataset,dependiente)
	ad = AD(dataset,paso1,paso2,paso3,paso4,paso5,paso6,paso7)

	if 'nuevo_registro' in request.GET:
		if request.GET['nuevo_registro'] == '1':
			data = {}
			for i in range(len(ad.get_columnas())):
				data[i] = [float(request.GET[ad.get_columnas()[i]])]
			ad.add_new_registro()
			ad.set_new_data(pd.DataFrame(data))

	return ad
