    function defaultSelected(){
        var archivo = document.getElementsByName("archivos")[0].value;
        var defaultVar = document.getElementsByName('archivos_default')[0];
        if(archivo == "default"){
            defaultVar.style.visibility='visible';
        }else{
            defaultVar.style.visibility='hidden';
        }
    }