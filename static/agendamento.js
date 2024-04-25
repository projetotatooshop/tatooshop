// Obtém a data atual
var hoje = new Date();

// Formata a data para o formato YYYY-MM-DD
var ano = hoje.getFullYear();
var mes = String(hoje.getMonth() + 1).padStart(2, '0');
var dia = String(hoje.getDate()).padStart(2, '0');
var minDate = ano + '-' + mes + '-' + dia;

// Define a data mínima no campo de entrada de data
document.getElementById('date').setAttribute('min', minDate);