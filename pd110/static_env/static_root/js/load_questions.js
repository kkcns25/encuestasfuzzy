
var encuesta = document.getElementById("encuesta").innerHTML;
document.getElementById("encuesta").innerHTML = '';

var questions = document.getElementById("questions").innerHTML;

questions = questions.slice(5,-6);
var txt = questions.split(',');

var i = 0;
var datos = [];
document.getElementById("questions").innerHTML = txt[i].slice(2, -1);

function cambiar_q(){
    i++;

    if(i<txt.length){
            document.getElementById("questions").innerHTML = txt[i].slice(2, -1);
    }

    var minpos = document.getElementById("slider_minmax_min").innerHTML;
    var maxpos = document.getElementById("slider_minmax_max").innerHTML;
    minpos = minpos.slice(4,);
    maxpos = maxpos.slice(4,);
    localStorage.setItem("Numero1", minpos);
    localStorage.setItem("Numero2", maxpos);
    datos[i-1]=minpos + '/' + maxpos;
    localStorage.setItem("datos", datos);

    if(i==txt.length){
        name = "/finished/?"+encuesta+'?'+datos;

        location = name;//En la pantalla finished se debería evaluar los datos del local storage y escribir en csv
    }

}

document.getElementById("boton").addEventListener('click', function(){
    cambiar_q();
});

document.write('<br>');


