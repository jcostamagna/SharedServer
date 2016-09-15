'use strict';

const express = require('express');
var path = require("path");

// Constants
const PORT = 8080;

// App
const app = express();

// Configuración
app.use(express.static(path.join(__dirname,'/WebApp')));


app.get('*', function(req, res) {  
    res.sendFile('WebApp/index.html');                
});


app.listen(process.env.PORT || PORT);
console.log('Running on http://localhost:' + PORT);
