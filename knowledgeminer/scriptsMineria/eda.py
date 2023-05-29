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
    paso2 = {
        'nulos':dataset.isnull().sum(),
        'info':first_info,
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
    print("Entrand a paso 3.1")
    for col in cols_atipicas:
        plt.clf()
        sns.boxplot(data=dataset[col],orient='h').set_title(col)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)
        graphs.append(uri)
    print("Entrand a paso 3.2")
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
    print("Entrand a paso 3.3")
    # Agrupación por variables categóricas
    agrupacion = []
    print(len(dataset.select_dtypes(include='object')))
    for col in dataset.select_dtypes(include='object'):
        if dataset[col].nunique() < 10:
        #Obtenemos la mediana de cada columna agregado por una sola columna.
            agrupacion.append(dataset.groupby(col).agg(['mean']))
    categoria_df = 0
    try:
        categoria_df = dataset.describe(include='object')
    except:
        categoria_df = 0
    paso3 = {
        'distribucion': uri,
        'descripcion': dataset.describe(),
        'atipicos': graphs,
        'categoricas_df': categoria_df,
        'categoricas': graphs_cat if len(graphs_cat) > 0 else -1 if len(graphs_cat) > 0 and len(categoria_df) > 0 else 0,
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
    dataset = dataset.iloc[0:500000]
    print("Entrando a paso 1")
    paso1 = descripcionEstructura(dataset)
    print("Entrando a paso 2")
    paso2 = datosFaltantes(dataset)
    print("Entrando a paso 3")
    paso3 = valoresAtipicos(dataset)
    print("Entrando a paso 4")
    paso4 = relaciones_variables(dataset)
    eda = EDA(dataset,paso1,paso2,paso3,paso4)
    return eda
