import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
import io
import sklearn
import urllib, base64
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from kneed import KneeLocator
from mpl_toolkits.mplot3d import Axes3D

class CLUSTERING():
	def __init__(self,dataset,paso1,paso2,paso3,columnas):
		self.dataset = dataset
		self.paso1 = paso1
		self.paso2 = paso2
		self.paso3 = paso3
		self.columnas = columnas
		self.new_registro = False

	def get_info(self):
		return self.paso1['info']

	def get_datos(self):
		return self.paso1['datos']

	def get_nuvDatos(self):
		return self.paso1['nuvDatos']

	def get_mCorr(self):
		return self.paso2['mCorr']

	def get_mStand(self):
		return self.paso3['mStand']

	def get_sse(self):
		return self.paso3['sse']
	def get_numK(self):
		return self.paso3['numK']

	def get_mPart(self):
		return self.paso3['mPart']

	def get_clustP(self):
		return self.paso3['clustP']

	def get_numElem(self):
		return self.paso3['numElem']

	def get_centros(self):
		return self.paso3['centros']

	def get_clusters(self):
		return self.paso3['clusters']
	
	def add_new_registro(self):
		self.new_registro = True
	
	def is_new_registro(self):
		return self.new_registro
	
	def set_new_data(self,data):
		self.new_data = data
	
	def predict_new(self):
		return self.paso3['kmeans'].predict(self.new_data)
	
	def get_new_data(self):
		return self.new_data
	
	def get_columnas(self):
		return self.columnas

def accesoDatos(dataset,dependiente):
	buffer = io.StringIO()
	dataset.info(buf=buffer)
	lines = buffer.getvalue().splitlines()[5:-2]
	info = [x.split(' ') for x in lines]
	info_new = []
	for i in info:
		line = []
		for j in i:
			if len(j) >= 1:
				line.append(j)
		info_new.append(line)
	first_info = []
	for i in info_new:
		line = []
		line.append(i[0]) #index
        #Find non-null
		non_null_index = i.index('non-null')
		non_null_index_minus = non_null_index-1
		string = ''
		for j in i[1:non_null_index_minus]:
			string+=j+' '
		line.append(string)
		line.append(i[non_null_index_minus]+' '+i[non_null_index])
		line.append(i[non_null_index+1])
		first_info.append(line)
	paso1 = {
		'info': first_info,
		'datos': dataset.groupby(dependiente).size(),
	}
	dataset.drop([dependiente], axis = 1, inplace = True)
	paso1['nuvDatos'] = dataset
	return paso1

def selCaract(dataset):
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
		'mCorr': uri,
	}
	return paso2

def segParticional(dataset):
	estandarizar = StandardScaler()
	MEstandarizada = estandarizar.fit_transform(dataset)
	#Definición de K clusters
	SSE = []
	for i in range(2, 10):
		km = KMeans(n_clusters=i, random_state=0)
		km.fit(MEstandarizada)
		SSE.append(km.inertia_)
	#Grafica SSE
	plt.clf()
	plt.figure(figsize=(10,7))
	plt.plot(range(2, 10), SSE, marker='o')
	plt.xlabel('Cantidad de clusters *k*')
	plt.ylabel('SSE')
	plt.title('Elbow Method')
	buf = io.BytesIO()
	plt.savefig(buf,format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())
	uri = urllib.parse.quote(string)
	buf.truncate(0)
	#Números de k clusters
	kl = KneeLocator(range(2, 10), SSE, curve="convex", direction="decreasing")
	num = kl.elbow
	#Etiquetas de los elementos.
	MParticional = KMeans(n_clusters=num, random_state=0).fit(MEstandarizada)
	MParticional.predict(MEstandarizada)
	dataset['clusterP'] = MParticional.labels_
	#Centroides.
	CentroidesP = dataset.groupby('clusterP').mean()
	#Grafica 3D de los elementos y los centros.
	plt.clf()
	plt.rcParams['figure.figsize'] = (10, 7)
	plt.style.use('ggplot')
	colores=['red', 'blue', 'green', 'yellow']
	asignar=[]
	for row in MParticional.labels_:
		asignar.append(colores[row])

	fig = plt.figure()
	ax = plt.axes(projection = "3d")
	ax.scatter3D(MEstandarizada[:, 0], 
    MEstandarizada[:, 1], 
    MEstandarizada[:, 2], marker='o', c=asignar, s=60)
	ax.scatter3D(MParticional.cluster_centers_[:, 0], 
    MParticional.cluster_centers_[:, 1], 
    MParticional.cluster_centers_[:, 2], marker='o', c=colores, s=1000)
	buf = io.BytesIO()
	plt.savefig(buf,format='png')
	buf.seek(0)
	string = base64.b64encode(buf.read())
	uri1 = urllib.parse.quote(string)
	buf.truncate(0)
	paso3 = {
		'mStand': pd.DataFrame(MEstandarizada),
		'sse': uri,
		'numK': num,
		'mPart': MParticional.labels_,
		'clustP': dataset,
		'numElem':dataset.groupby(['clusterP'])['clusterP'].count(),
		'centros': CentroidesP,
		'clusters': uri1,
		'kmeans':MParticional,
	}
	return paso3

def initialization(file_path,dependiente,request):
	dataset = pd.read_csv(file_path)
	dataset = dataset
	columnas = dataset.columns.tolist()
	columnas.remove(dependiente)
	paso1 = accesoDatos(dataset,dependiente)
	paso2 = selCaract(dataset)
	paso3 = segParticional(dataset)
	clustering = CLUSTERING(dataset,paso1,paso2,paso3,columnas=columnas)
	if 'nuevo_registro' in request.GET:
		if request.GET['nuevo_registro'] == '1':
			data = {}
			for i in range(len(columnas)):
				data[i] = [float(request.GET[columnas[i]])]
			clustering.add_new_registro()
			clustering.set_new_data(pd.DataFrame(data))
	return clustering