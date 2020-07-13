
document.write('esto esta escrito desde script');

/*
var encuesta = document.getElementById("encuesta").innerHTML;
document.getElementById("encuesta").innerHTML = '';
document.write(encuesta);*/
var questions = document.getElementById("questions").innerHTML;
//var resultados = [[1,2,3,4],[5,6,7,8],[9,10,11,12]];
var resultados = document.getElementById("resultados").innerHTML;
document.write(resultados);
questions = questions.slice(0,-1);
var txt = questions.split(',');
var i=0;
var f='';

for(i=0; i< txt.length; i++){
    txt[i]=txt[i].slice(2, -1);
 }

i = 0;
document.getElementById("questions").innerHTML = txt[i];
Plotly.newPlot('plotlyChart', datos(i));
function  datos(i) {

          var data = [
            {
              // x:   no hace falta el eje i
              y: resultados[i],
              type: 'scatter'
            }
          ];
    return data;
}

function cambiar_q(f){

    if(f=='0'){
        if(i<(txt.length-1)){
            i++;
            document.getElementById("questions").innerHTML = txt[i];
            Plotly.newPlot('plotlyChart', datos(i));
        }
    }

    if(f=='1'){
        if(i>0){
            i--;
            document.getElementById("questions").innerHTML = txt[i];
            Plotly.newPlot('plotlyChart', datos(i));
        }
    }

}


document.getElementById("boton2").addEventListener('click', function(){
cambiar_q('1');});
document.getElementById("boton").addEventListener('click', function(){
cambiar_q('0');});

document.write('<br>');
document.write('hasta aquí con javascript');

