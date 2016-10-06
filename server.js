'use strict';

const express = require('express');
var path = require("path");
const pg = require('pg');
var bodyParser = require('body-parser')

// Constants
const PORT = 8080;

// App
const app = express();

pg.defaults.ssl = true;


//app.use(bodyParser());

app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
})); 
//~ app.use( bodyParser.json() );       // to support JSON-encoded bodies
//app.use(bodyParser.urlencoded({ extended: true }))    // parse application/x-www-form-urlencoded
app.use(bodyParser.json())    // parse application/json

const connectionString = process.env.DATABASE_URL || 'postgres://koicdmjsauxtuc:2juyGj1IcOMLPrbK_vhaBj0v5V@ec2-54-221-225-242.compute-1.amazonaws.com:5432/debpfqvr21od6g';

const client = new pg.Client(connectionString);
client.connect();
const query = client.query(
  'CREATE TABLE IF NOT EXISTS categorias(nombre VARCHAR(40) PRIMARY KEY, descripcion VARCHAR(140))');
query.on('end', () => { client.end(); });


// Configuración
app.use(express.static(path.join(__dirname,'/WebApp')));

app.get('/test', function(req, res) {
	const results = [];
	pg.connect(connectionString, (err, client, done) => {
    // Handle connection errors
    if(err) {
      done();
      console.log(err);
      return res.status(404).json({success: false, data: err, context: '/test'});
    }
    // SQL Query > DELETE Data
    client.query('DELETE FROM categorias');
    // SQL Query > Select Data
    const query = client.query('SELECT * FROM categorias');
    // Stream results back one row at a time
    query.on('row', (row) => {
      results.push(row);
    });
    // After all data is returned, close connection and return results
    query.on('end', () => {
      done();
      return res.status(201).json(results);
    });
  });
    //res.write('Prueba GET');
    //res.end();                
});

app.get('*', function(req, res) {  
    res.sendFile('WebApp/index.html');                
});

app.get('/categories', (req, res, next) => {
  const results = [];
  // Grab data from http request
  // Get a Postgres client from the connection pool
  pg.connect(connectionString, (err, client, done) => {
    // Handle connection errors
    if(err) {
      done();
      console.log(err);
      return res.status(500).json({success: false, data: err, context: '/categories'});
    }
    // SQL Query > Select Data
    const query = client.query('SELECT * FROM categorias');
    // Stream results back one row at a time
    query.on('row', (row) => {
      results.push({'name':row[0], 'description':row[1]});
    });
    // After all data is returned, close connection and return results
    query.on('end', () => {
      done();
    });
  });
  //res.setHeader('Content-Type', 'application/json');
  return res.status(201).json({'categories':results, 'metadata': {'count':0}});
});


app.delete('/categories/:category', function (req, res) {
	console.log(req.params.category)
  res.send('DELETE request to homepage');
});


app.post('/categories', (req, res, next) => {
  const results = [];
  // Grab data from http request
  //~ console.log(req.body);
  //~ console.log(req.header);
  //~ console.log(req.body.category.name);
  //~ console.log(req.body.category.description);
  const data = {nombre: req.body.category.name, descripcion: req.body.category.description};
  // Get a Postgres client from the connection pool
  pg.connect(connectionString, (err, client, done) => {
    // Handle connection errors
    if(err) {
      done();
      console.log(err);
      return res.status(500).json({success: false, data: err, context: '/categories'});
    }
    // SQL Query > Insert Data
    client.query('INSERT INTO categorias(nombre, descripcion) values($1, $2)',
    [data.nombre, data.descripcion]);
    // SQL Query > Select Data
    /*const query = client.query('SELECT * FROM categorias');
    // Stream results back one row at a time
    query.on('row', (row) => {
      results.push(row);
    });*/
    // After all data is returned, close connection and return results
    query.on('end', () => {
      done();
    });
  });
  //res.setHeader('Content-Type', 'application/json');
  return res.status(201).json(req.body);
});


app.listen(process.env.PORT || PORT);
console.log('Running on http://localhost:' + PORT);
