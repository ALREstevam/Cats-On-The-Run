/**
 * Created by andre on 31/10/2018.
 */


var estadoLampada = 'apagada';
var estaQueimada = false;

function getLampada() {
    return document.getElementById('lampada')
}
//Usando eventListner
getLampada().addEventListener("dblclick", queima);

function inverteEstado() {
    console.log('Mudando estado da lampada');
    if(estadoLampada=="apagada"){
        acende();
    }
    else if(estadoLampada=="acesa"){
        apaga();
    }
}

function acende() {
    console.log('Tentando acender');
    if(!estaQueimada){
        estadoLampada='acesa';
        getLampada().src="on.jpg"
    }
}
function apaga() {
    console.log('Tentando apagar');
    if(!estaQueimada){
        estadoLampada='apagada';
        getLampada().src="off.jpg"
    }
}
function queima() {
    estaQueimada = true;
    getLampada().src="broken.jpg"
}




















/*

console.warn('EXECUTANDO O COMANDO document.getElementById("div1")');
var a = document.getElementById("div1");
console.log(a);



console.warn('EXECUTANDO O COMANDO document.getElementsByClassName("styled")');
var b  = document.getElementsByClassName("styled");
console.log(b);



console.warn('EXECUTANDO O COMANDO document.getElementsByName("username")');
var c =  document.getElementsByName("username");
console.log(c);



console.warn('EXECUTANDO O COMANDO document.getElementsByTagName("P")');
var d =  document.getElementsByTagName("P");
console.log(d);



function change() {
    console.warn('Substituindo o conteúdo de quem tem o id=div1');
    document.getElementById("div1").innerHTML = "<H1>OLÁ</H1>";

    console.warn('Mudando o fundo de todo elemento com a classe styled');
    for (var i = 0; i < document.getElementsByClassName("styled").length; i++){
        document.getElementsByClassName("styled")[i].style.backgroundColor = '#ff0000';
    }

    console.warn('Mudando o campo value de todo elemento com name="username"');
    for (var i = 0; i < document.getElementsByName("username").length; i++){
        var valorAntigo = document.getElementsByName("username")[i].value;
        document.getElementsByName("username")[i].setAttribute('value','MUDOU! ' + valorAntigo);
    }

    console.warn('Mudando o texto de toda sas tags do tipo P');
    for (var i = 0; i < document.getElementsByTagName("P").length; i++){
        document.getElementsByTagName("P")[i].innerText = "NOVO TEXTO"
    }
}

*/