import pandas as pd               # Para la manipulación y análisis de datos
import numpy as np                # Para crear vectores y matrices n dimensionales
import matplotlib.pyplot as plt   # Para la generación de gráficas a partir de los datos
import seaborn as sns             # Para la visualización de datos basado en matplotlib
import io

class EDA():

    def __init__(self,dataset,paso1,paso2,paso3,paso4):
        self.dataset = dataset
        self.paso1 = paso1
        self.paso2 = paso2

    def get_forma(self):
        return self.paso1['forma']
    
    def get_tipo_dato(self):
        return self.paso1['tipo_dato']
    
    def get_nulos(self):
        return self.paso2['nulos']
    
    def get_info(self):
        return self.paso2['info']


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

def initialization(file_path):
    dataset = pd.read_csv(file_path)
    paso1 = descripcionEstructura(dataset)
    paso2 = datosFaltantes(dataset)
    eda = EDA(dataset,paso1,paso2,'','')
    return eda
