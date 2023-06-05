from sklearn.metrics import RocCurveDisplay
from sklearn import metrics
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import io
import urllib, base64
from sklearn.preprocessing import LabelBinarizer
import numpy as np
from itertools import cycle
from sklearn.metrics import roc_curve, auc
import seaborn as sns

class Validacion:

    def __init__(self,arbol,bosque,var_dep):
        self.arbol = arbol
        self.bosque = bosque
        self.var_dep = var_dep
    
    def get_accuracies(self):
        return [self.arbol.get_accuracy(),self.bosque.get_accuracy()]
    
    def get_ROC(self):
        graphs = []
        if len(np.unique(self.arbol.get_Y_validation())) == 2:
            fig, ax = plt.subplots()
            buf = io.BytesIO()
            RocCurveDisplay.from_estimator(self.arbol.get_arbol(),
                                           self.arbol.get_X_validation(),
                                           self.arbol.get_Y_validation(),
                                           ax = ax
                                           )
            metrics.RocCurveDisplay.from_estimator(self.bosque.get_bosque(),
                                    self.bosque.get_X_validation(),
                                    self.bosque.get_Y_validation(),
                                    ax = ax)
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            graphs.append(uri)
            buf.truncate(0)
        else:
            fig, ax = plt.subplots()
            buf = io.BytesIO()
            y_score = self.arbol.get_arbol().predict_proba(self.arbol.get_X_validation())
            label_binarizer = LabelBinarizer()
            y_test_bin = label_binarizer.fit_transform(self.arbol.get_Y_validation())
            fpr = dict()
            tpr = dict()
            roc_auc = dict()
            n_classes = len(np.unique(self.arbol.get_Y_validation()))
            colors = sns.color_palette("hls", n_classes)
            print(n_classes)
            for i in range(n_classes):
                fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
                roc_auc[i] = auc(fpr[i], tpr[i])
                plt.plot(fpr[i], tpr[i], color=colors[i], lw=2, label='Curva ROC de la clase {0} (area ={1:0.2f})'.format(i,roc_auc[i]))
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.title('Curvas ROC del Árbol de clasificación')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.legend(loc="lower right")
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            graphs.append(uri)
            buf.truncate(0)

            fig, ax = plt.subplots()
            buf = io.BytesIO()
            y_score = self.bosque.get_bosque().predict_proba(self.bosque.get_X_validation())
            label_binarizer = LabelBinarizer()
            y_test_bin = label_binarizer.fit_transform(self.bosque.get_Y_validation())
            fpr = dict()
            tpr = dict()
            roc_auc = dict()
            n_classes = len(np.unique(self.bosque.get_Y_validation()))
            colors = sns.color_palette("Paired", n_classes)
            print(n_classes)
            for i in range(n_classes):
                fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_score[:, i])
                roc_auc[i] = auc(fpr[i], tpr[i])
                plt.plot(fpr[i], tpr[i], color=colors[i], lw=2, label='Curva ROC de la clase {0} (area ={1:0.2f})'.format(i,roc_auc[i]))
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.title('Curvas ROC del Bosque Aleatorio')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.legend(loc="lower right")
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)
            graphs.append(uri)
            buf.truncate(0)
        return graphs
    

def initialization(arbol, bosque,var_dep):
    return Validacion(arbol,bosque,var_dep)
