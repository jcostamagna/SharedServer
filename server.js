'use strict';

const express = require('express');
var path = require("path");
const pg = require('pg');
var bodyParser = require('body-parser');
var categories = require("./js/categories");
var skills = require("./js/skills");
var toobusy = require('toobusy-js');

// Constants
const PORT = 8080;

// App
const app = express();

pg.defaults.ssl = true;

// middleware which blocks requests when we're too busy
app.use(function(req, res, next) {
  if (toobusy()) {
    res.send(500, "I'm busy right now, sorry.");
    console.log("I'm busy right now, sorry.");
  } else {
    next();
  }
});


app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
})); 
app.use(bodyParser.json());    // parse application/json

/*
//~ var connectionString = process.env.DATABASE_URL || 'postgres://koicdmjsauxtuc:2juyGj1IcOMLPrbK_vhaBj0v5V@ec2-54-221-225-242.compute-1.amazonaws.com:5432/debpfqvr21od6g';
var connectionString = process.env.DATABASE_URL || 'postgres://juan:12Oct1993@localhost:5432/sharedServer?sslmode=require';
//~ var connectionString = process.env.DATABASE_URL || 'postgres://uvwiyhoazhndqk:28c0drCwyXJILkCJMxjHz38LDq@ec2-23-23-225-98.compute-1.amazonaws.com:5432/dfp1uurfqcikj2';


var client = new pg.Client(connectionString);
client.connect();
var query = client.query(
  'CREATE TABLE IF NOT EXISTS categorias(nombre VARCHAR(40) PRIMARY KEY, descripcion VARCHAR(140))');
query.on('end', () => { client.end(); });
*/
//app.locals.connectionString = connectionString;
//app.locals.client = client;
//app.set('connectionString', connectionString);
//app.set('client', client);
//categories.iniciar(connectionString, client);

// Configuración
app.use(express.static(path.join(__dirname,'/WebApp')));



app.get('/', function(req, res) { 
    res.sendFile('WebApp/index.html');                
});

app.use('/categories', categories);

app.use('/skills', skills);

var server = app.listen(process.env.PORT || PORT);
console.log('Running on http://localhost:' + PORT);

process.on('SIGINT', function() {
  server.close();
  // calling .shutdown allows your process to exit normally
  toobusy.shutdown();
  process.exit();
});