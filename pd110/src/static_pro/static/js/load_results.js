
var questions = document.getElementById("questions").innerHTML;
var resultados = document.getElementById("resultados").innerHTML;
resultados = trans_resultados(resultados);

document.getElementById("resultados").innerHTML = '';
questions = questions.slice(0,-1);
var txt = questions.split(',');
var i=0;
var f='';

for(i=0; i< txt.length; i++){
    txt[i]=txt[i].slice(2, -1);
 }

var layout = { //Especificamos los rangos de los ejes
    xaxis: {
        range: [0, 100]
    },
    yaxis: {
        range: [0, 100]
    },
};

function trans_resultados(resultados){
    resultados = resultados.slice(2,-2);
    resultados = resultados.split('], [');

    for (i=0; i< resultados.length; i++){
        resultados[i]=resultados[i].split(', ');

        for (j=0; j< resultados[i].length; j++){
            resultados[i][j]= parseInt(resultados[i][j], 10);
            }
  }
    return resultados;
}

i = 0;
document.getElementById("questions").innerHTML = txt[i];
Plotly.newPlot('plotlyChart', datos(i), layout);
function  datos(i) {

          var data = [
            {
              // x:   no hace falta el eje i
              y: resultados[i],
              type: 'scatter',
              line: {shape: 'spline',smoothing: 0.2}// para los bordes redondeados de las curvas, que no sean lineas rectas(entre0 y 1.3)
            }
          ];
    return data;
}

function cambiar_q(f){

    if(f=='0'){
        if(i<(txt.length-1)){
            i++;
            document.getElementById("questions").innerHTML = txt[i];
            Plotly.newPlot('plotlyChart', datos(i), layout);
        }
    }

    if(f=='1'){
        if(i>0){
            i--;
            document.getElementById("questions").innerHTML = txt[i];
            Plotly.newPlot('plotlyChart', datos(i), layout);
        }
    }

}


document.getElementById("boton2").addEventListener('click', function(){
cambiar_q('1');});
document.getElementById("boton").addEventListener('click', function(){
cambiar_q('0');});

document.write('<br>');


