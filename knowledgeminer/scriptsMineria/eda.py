import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
import io
import urllib, base64

class EDA():

    def __init__(self,dataset,paso1,paso2,paso3,paso4):
        self.dataset = dataset
        self.paso1 = paso1
        self.paso2 = paso2
        self.paso3 = paso3
        self.paso4 = paso4

    def get_forma(self):
        return self.paso1['forma']
    
    def get_tipo_dato(self):
        return self.paso1['tipo_dato']
    
    def get_nulos(self):
        return self.paso2['nulos']
    
    def get_info(self):
        return self.paso2['info']
    
    def get_distribucion(self):
        return self.paso3['distribucion']

    def get_resumen(self):
        return self.paso3['descripcion']
    
    def get_diagramas_atipicos(self):
        return self.paso3['atipicos']
    
    def get_categoricas_df(self):
        return self.paso3['categoricas_df']
    
    def get_categoricas(self):
        return self.paso3['categoricas']
    
    def get_agrupacion(self):
        return self.paso3['agrupacion']
    
    def get_corr(self):
        return self.paso4['corr']
    
    def get_corr_graph(self):
        return self.paso4['graph_corr']
    
    def get_corr_inf(self):
        return self.paso4['graph_inf']

def descripcionEstructura(dataset):
    paso1 = {
        'forma': dataset.shape,
        'tipo_dato': dataset.dtypes
    }
    return paso1

def datosFaltantes(dataset):
    buffer = io.StringIO()
    dataset.info(buf=buffer)
    lines = buffer.getvalue().splitlines()
    df = (pd.DataFrame([x.split() for x in lines[5:-2]], columns=lines[3].split())
       .drop('Count',axis=1)
       .rename(columns={'Non-Null':'Non-Null Count'}))
    paso2 = {
        'nulos':dataset.isnull().sum(),
        'info':df
    }
    return paso2

def get_outliers(dataset):
    q1=dataset.quantile(0.25)
    q3=dataset.quantile(0.75)
    IQR=q3-q1
    outliers = dataset[((dataset<(q1-1.5*IQR)) | (dataset>(q3+1.5*IQR)))]
    columns = []
    for i in outliers.columns:
        if outliers[i].isnull().sum() < dataset.shape[0]:
            columns.append(i)
    return columns

def valoresAtipicos(dataset):
    #Obtención de distribución de variables
    dataset.hist(figsize=(14,14), xrot=45)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    #Obtención de histograma de valores atípicos
    cols_atipicas = get_outliers(dataset)
    graphs = []
    for col in cols_atipicas:
        plt.clf()
        sns.boxplot(data=dataset[col],orient='h').set_title(col)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        graphs.append(uri)

    #Variables categóricas
    graphs_cat = []
    for col in dataset.select_dtypes(include='object'):
        if dataset[col].nunique()<10:
            plt.clf()
            sns.countplot(y=col, data=dataset).set_title(col)
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            graphs_cat.append(uri)
    
    # Agrupación por variables categóricas
    agrupacion = []
    for col in dataset.select_dtypes(include='object'):
        if dataset[col].nunique() < 10:
        #Obtenemos la mediana de cada columna agregado por una sola columna.
            agrupacion.append(dataset.groupby(col).agg(['mean']))
    paso3 = {
        'distribucion': uri,
        'descripcion': dataset.describe(),
        'atipicos': graphs,
        'categoricas_df': dataset.describe(include='object'),
        'categoricas': graphs_cat,
        'agrupacion': agrupacion,
    }
    return paso3

def relaciones_variables(dataset):
    plt.clf()
    plt.figure(figsize=(14,7))
    sns.heatmap(dataset.corr(), cmap='RdBu_r', annot=True)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)

    plt.clf()
    plt.figure(figsize=(14,7))
    MatrizInf = np.triu(dataset.corr())
    sns.heatmap(dataset.corr(), cmap='RdBu_r', annot=True, mask=MatrizInf)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri2 = urllib.parse.quote(string)

    paso4 = {
        'corr': dataset.corr(),
        'graph_corr': uri,
        'graph_inf': uri2,
    }
    return paso4

def initialization(file_path):
    dataset = pd.read_csv(file_path)
    paso1 = descripcionEstructura(dataset)
    paso2 = datosFaltantes(dataset)
    paso3 = valoresAtipicos(dataset)
    paso4 = relaciones_variables(dataset)
    eda = EDA(dataset,paso1,paso2,paso3,paso4)
    return eda
