var http = require("http");
var url = require("url");
var express     = require('express');  
var app         = express();

function iniciar(route, handle) {
  function onRequest(request, response) {
        var dataPosteada = "";
        var pathname = url.parse(request.url).pathname;
        console.log("Peticion para " + pathname + " recibida.");

        request.setEncoding("utf8");

        request.addListener("data", function(trozoPosteado) {
          dataPosteada += trozoPosteado;
          console.log("Recibido trozo POST '" + trozoPosteado + "'.");
    });

    request.addListener("end", function() {
      route(handle, pathname, response, dataPosteada);
    });

  }

  http.createServer(onRequest).listen(process.env.PORT || 5000);
  console.log("Servidor Iniciado");
}

// Carga una vista HTML simple donde irá nuestra Single App Page
// Angular Manejará el Frontend
app.get('*', function(req, res) {  
    res.sendfile('./public/index.html');                
});

exports.iniciar = iniciar;
