    function defaultSelected(){
        var archivo = document.getElementsByName("archivos")[0].value;
        var defaultVar = document.getElementsByName('archivos_default')[0];
        if(archivo == "default"){
            defaultVar.style.visibility='visible';
        }else{
            defaultVar.style.visibility='hidden';
        }
    }

    function selectedAlgorithm(){
        var algoritmo = document.getElementsByName("algoritmo")[0].value;
        var archivo = document.getElementsByName("archivos");
        for( i = 0; i < archivo.length; i++){
            document.getElementById(archivo[i].value).style.visibility = 'hidden';
        }
        if(algoritmo == "ad" || algoritmo == "ba"){
            if(archivo[0].value != "Seleccione archivo")
                document.getElementById(archivo[0].value).style.visibility = 'visible';
        }
    }