'use strict';

const express = require('express');
var path = require("path");

// Constants
const PORT = 8080;

// App
const app = express();

// Configuración
app.use(express.static(path.join(__dirname,'/WebApp')));

// Rutas de nuestro API
// GET de todos los TODOs
app.get('/job_positions', function(req, res) {  
	console.log("GET job positions");
});

// POST que crea un TODO y devuelve todos tras la creación
app.post('/job_positions', function(req, res) {  
	console.log("POST");
	console.log("Parametros:" + req.body.text);
});

// PUT que modifica una fila
app.put('/job_positions/categories/development/developer', function(req, res) {  
	console.log("PUT");
	console.log("Parametros:" + req.body.text);
});

// DELETE un TODO específico y devuelve todos tras borrarlo.
app.delete('/job_positions/:todo', function(req, res) {  
	console.log("DELETE");
	console.log("Parametros:" + req.params.todo);
});

app.get('*', function(req, res) {  
    res.sendFile('WebApp/index.html');                
});


app.listen(process.env.PORT || PORT);
console.log('Running on http://localhost:' + PORT);
