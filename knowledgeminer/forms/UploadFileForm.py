from django import forms

class UploadFileForm(forms.Form):
    titulo = forms.CharField(max_length=50, label="Escriba nombre del archivo")
    archivo = forms.FileField(label='Selecciona un archivo que desea utilizar')