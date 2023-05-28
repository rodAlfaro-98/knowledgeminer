function defaultSelected(){
    var archivo = document.getElementsByName("archivos")[0].value;
    if(archivo.value == "default"){
        alert('default');
        document.getElementsByName('archivos_default').style.visibility='visible';
    }
}