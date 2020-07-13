
document.write('escrito con script de javaScript, eliminar load_encuestas.js si no se usa');
/*

var loc = document.URL;
        // si existe nombre del documento pasado por la url
    if(loc.indexOf('#')==0){location = "/inicio/";}
    if(loc.indexOf('#')>0)
    {   // cogemos la parte de la url que hay despues del interrogante
        var arch = loc.split('#')[1];
        var arch1 = arch.replace('%20', ' ');

        while(arch != arch1){
            arch = arch1;
            arch1 = arch1.replace('%20', ' ');
        }
    }
    var nombre = arch;
    arch = arch + '.csv';
    arch2 = '/read_r/#'+arch;

    document.getElementById("question").innerHTML = arch2;
    document.getElementById("encuesta").innerHTML = 'qweqeqe';

      para probar local storage, borrar
    localStorage.setItem('encuesta', arch);

    var nombre = localStorage.getItem('encuesta');
    nombre = nombre.slice(0, -4);


document.write('<h1>Vamos a ver sus resultados de la encuesta: ' + nombre + "<\h1>");
document.write('<a class="btn btn-lg btn-primary" href="{% url 'read_r' %}?'+arch+'"role="button">Comenzar &raquo;</a>');
*/
/*Da problemas, no carga bien el enlace aunque esta bien creado, se deja en script de html




var encuestas = document.getElementById("encuestas").innerHTML;
document.getElementById("encuestas").innerHTML = "";

encuestas = encuestas.slice(0,-7);
var txt = encuestas.split('.csv');
txt[0] = ' '+txt[0];

for (var i = 0; i < txt.length; i++) {

    texto = txt[i].slice(4);
    texto1 = String(texto + " &raquo;</a><br/>");
    texto2 = String('<br/><a class="btn btn-lg btn-primary" href="{% url ');
    texto2 = String(texto2 + "'start_q' %}?");texto2 = String(texto2 + texto);
    texto2 = String(texto2 + '" role="button">');
    texto2 = String(texto2 + texto1);
    console.log(texto2);

    document.write(texto2);
    //document.write('<input type="hidden" name="campo1" value="3005">');
}

*/