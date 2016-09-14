'use strict';

const express = require('express');
var path = require("path");
// Constants
const PORT = 8080;

// App
const app = express();
//app.get('/', function (req, res) {
//    res.send('Hello world\n');
//});

// Configuración
    // Localización de los ficheros estÃ¡ticos
    app.use(express.static(path.join(__dirname,'/WebApp')));
    // Muestra un log de todos los request en la consola        
   // app.use(express.logger('dev')); 
    // Permite cambiar el HTML con el método POST                   
  //  app.use(express.bodyParser());
    // Simula DELETE y PUT                      
  //  app.use(express.methodOverride());  

app.get('*', function(req, res) {  
    res.sendFile('WebApp/index.html');                
});

app.listen(process.env.PORT || PORT);
console.log('Running on http://localhost:' + PORT);
