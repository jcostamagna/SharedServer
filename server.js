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


app.use(bodyParser.urlencoded({     // to support URL-encoded bodies
  extended: true
})); 
app.use(bodyParser.json())    // parse application/json

//~ var connectionString = process.env.DATABASE_URL || 'postgres://koicdmjsauxtuc:2juyGj1IcOMLPrbK_vhaBj0v5V@ec2-54-221-225-242.compute-1.amazonaws.com:5432/debpfqvr21od6g';
//~ var connectionString = process.env.DATABASE_URL || 'postgres://juan:12Oct1993@localhost:5432/sharedServer?sslmode=require';
var connectionString = process.env.DATABASE_URL || 'postgres://uvwiyhoazhndqk:28c0drCwyXJILkCJMxjHz38LDq@ec2-23-23-225-98.compute-1.amazonaws.com:5432/dfp1uurfqcikj2';


var client = new pg.Client(connectionString);
client.connect();
var query = client.query(
  'CREATE TABLE IF NOT EXISTS categorias(nombre VARCHAR(40) PRIMARY KEY, descripcion VARCHAR(140))');
query.on('end', () => { client.end(); });


// Configuración
app.use(express.static(path.join(__dirname,'/WebApp')));

app.get('/test', function(req, res) {
	pg.connect(connectionString, function(err, client, done) {
    // Handle connection errors
    if(err) {
      done();
      console.log(err);
      return res.status(404).json({success: false, data: err, context: '/test'});
    }
    
    // SQL Query > DELETE Data
    var query = client.query('DELETE FROM categorias');

    // After all data is returned, close connection and return results
	query.on('end', function() {
		done();
		return res.status(201).json([]);
	});
  });
             
});

app.get('/', function(req, res) { 
    res.sendFile('WebApp/index.html');                
});


app.get('/categories', function(req, res, next) {
	var rows = {};
	rows['categories'] = [];
	rows['metadata'] = {};
	var registro = {};
	
	// Get a Postgres client from the connection pool
	pg.connect(connectionString, function(err, client, done) {
    // Handle connection errors
		if(err) {
			done();
			console.log(err);
			return res.status(500).json({success: false, data: err, context: '/categories'});
		}
    
		var length = 0;
		// SQL Query > Select Data
		var query = client.query('SELECT * FROM categorias');
		// Stream results back one row at a time
		query.on('row', function(row) {
			registro = {};
			registro['name'] = row.nombre;
			registro['description'] = row.descripcion;
			//console.log(registro);
			rows['categories'].push(registro);
			length += 1;
			//results.push({'name':row.nombre, 'description':row.descripcion}.toObject());
			//console.log({'name':row.nombre, 'description':row.descripcion});
		});
		
		// After all data is returned, close connection and return results
		query.on('end', function() {
			done();
			rows['metadata']['count'] = length;
			//console.log(rows);
			return res.status(201).json(rows);
		});
	});
});


app.delete('/categories/:category', function (req, res) {
	pg.connect(connectionString, function(err, client, done) {
    // Handle connection errors
    if(err) {
      done();
      console.log(err);
      return res.status(404).json({success: false, data: err, context: '/test'});
    }
    // SQL Query > DELETE Data
    var query = client.query("DELETE FROM categorias WHERE nombre IN ($1)", [req.params.category]);

    // After all data is returned, close connection and return results
	query.on('end', function() {
		done();
		return res.status(204).json({});
	});
  
	
  });

});


app.post('/categories', function(req, res, next){
  // Grab data from http request
  var data = {nombre: req.body.category.name, descripcion: req.body.category.description};
  
  // Get a Postgres client from the connection pool  
  pg.connect(connectionString, function(err, client, done) {
    // Handle connection errors
    if(err) {
      done();
      console.log(err);
      return res.status(500).json({success: false, data: err, context: '/categories'});
    }
    // SQL Query > Insert Data
    var query = client.query('INSERT INTO categorias(nombre, descripcion) values($1, $2)',
    [data.nombre, data.descripcion]);
    
    query.on('error', function(err) {
		return res.status(500).json({success: false, data: err, context: '/categories'});
	});

        // After all data is returned, close connection and return results
	query.on('end', function() {
		done();
		return res.status(201).json(req.body);
	});
  });

});

//Update Category
app.post('/categories/:category', function(req, res, next){
  // Grab data from http request
  var category = req.params.category;
  var data = {nombre: req.body.category.name, descripcion: req.body.category.description};
  
  // Get a Postgres client from the connection pool  
  pg.connect(connectionString, function(err, client, done) {
    // Handle connection errors
    if(err) {
      done();
      console.log(err);
      return res.status(500).json({success: false, data: err, context: '/categories'});
    }
    // SQL Query > Insert Data
    var query = client.query('UPDATE categorias SET nombre=($1), descripcion=($2) WHERE nombre=($3)',
    [data.nombre, data.descripcion, category]);
    
    query.on('error', function(err) {
		return res.status(500).json({success: false, data: err, context: '/categories'});
	});

    // After all data is returned, close connection and return results
	query.on('end', function() {
		done();
		return res.status(201).json(req.body);
	});
  });

});


app.listen(process.env.PORT || PORT);
console.log('Running on http://localhost:' + PORT);
