var columnas = new Set();
var columnas_array = []
var porcentaje = 0;

function defaultSelected(){
    var archivo = document.getElementsByName("archivos")[0].value;
    var defaultVar = document.getElementsByName('archivos_default')[0];
    if(archivo == "default"){
        defaultVar.style.display='block';
    }else{
        defaultVar.style.display='none';
    }
}

function selectedAlgorithm(){
    var algoritmo = document.getElementsByName("algoritmo")[0].value;
    var archivo = document.getElementsByName("archivos");
    document.getElementById('dependiente').style.display='none';
    for( i = 0; i < archivo.length; i++){
        document.getElementById(archivo[i].value).style.display='none';
    }
    if(algoritmo == "ad" || algoritmo == "ba"){
        if(archivo[0].value != "Seleccione archivo"){
            document.getElementById('dependiente').style.display='block';
            document.getElementById(archivo[0].value).style.display='block';
        }
    }
}

function getCargas(){
    columnas = new Set();
    var table = document.getElementById('cargas');
    porcentaje = 0
    porcentaje = document.getElementById("porcentaje_carga").value;
    for( var r = 0, n = table.rows.length; r < n; r++){
        for(var c = 0, m = table.rows[r].cells.length; c < m; c++){
            if(table.rows[r].cells[c].innerHTML >= (porcentaje/100)){
                table.rows[r].cells[c].style.backgroundColor  = "#D6EEEE";
                columnas.add(table.rows[0].cells[c].innerHTML);
            }else{
                table.rows[r].cells[c].style.backgroundColor  = "#FFFFFF";
            }
        }
    }
    if(columnas.size > 0){
        document.getElementById('cargas_header').style.display='block';
        document.getElementById('span_cargas').innerHTML = 'Las columnas con cargas importantes son:';
        columnas_array = Array.from(columnas)
        document.getElementById('valores_cargas').innerHTML = columnas_array.toString();
    }else{
        document.getElementById('span_cargas').innerHTML = 'No se cuentan con columnas que cumplan con el porcentaje seleccionado';
        document.getElementById('valores_cargas').innerHTML = '';
    }

}

function getURLCargas(){
    return window.location.replace('../../knowledgeminer/export/pca/'+columnas_array+'/'+porcentaje.toString());
}