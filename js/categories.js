/**
 * Created by juan on 8/11/16.
 */

var express = require('express');
var router = express.Router();
const pg = require('pg');

pg.defaults.ssl = true;
//~ var connectionString = process.env.DATABASE_URL || 'postgres://koicdmjsauxtuc:2juyGj1IcOMLPrbK_vhaBj0v5V@ec2-54-221-225-242.compute-1.amazonaws.com:5432/debpfqvr21od6g';
//var connectionString = process.env.DATABASE_URL || 'postgres://juan:12Oct1993@localhost:5432/sharedServer?sslmode=require';
var connectionString = process.env.DATABASE_URL || 'postgres://uvwiyhoazhndqk:28c0drCwyXJILkCJMxjHz38LDq@ec2-23-23-225-98.compute-1.amazonaws.com:5432/dfp1uurfqcikj2';
var client = new pg.Client(connectionString);
client.connect();

/*var query = client.query(
    'DROP TABLE IF EXISTS categorias');
query.on('end', () => { client.end(); });*/

var query = client.query(
    'CREATE TABLE IF NOT EXISTS categorias(nombre VARCHAR(40) PRIMARY KEY, descripcion VARCHAR(140))');
query.on('end', () => { client.end(); });


//Funcion de testeo para limpiar la tabla de categorias
router.get('/test', function(req, res) {
    pg.connect(connectionString, function(err, client, done) {
        // Handle connection errors
        if(err) {
            done();
            console.log(err);
            return res.status(404).json({code: 0, message: err});
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

//GET categorias
router.get('/', function(req, res) {
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
            return res.status(500).json({code: 0, message: err});
        }

        var length = 0;
        // SQL Query > Select Data
        var query = client.query('SELECT * FROM categorias');
        // Stream results back one row at a time
        query.on('row', function(row) {
            registro = {};
            registro['name'] = row.nombre;
            registro['description'] = row.descripcion;
            rows['categories'].push(registro);
            length += 1;
        });

        // After all data is returned, close connection and return results
        query.on('end', function() {
            done();
            rows['metadata']['count'] = length;
            rows['metadata']['version'] = "0.1";
            return res.status(201).json(rows);
        });
    });
});

//DELETE categoria
router.delete('/:category', function (req, res) {
    if (req.params.category == undefined ){
        return res.status(400).json({code: 0, message: 'Faltan parametros'});
    }
    pg.connect(connectionString, function(err, client, done) {
        // Handle connection errors
        if(err) {
            done();
            console.log(err);
            return res.status(404).json({code: 0, message: err});
        }
        var rowsAffected;
        // SQL Query > DELETE Data
        var query = client.query("DELETE FROM categorias WHERE nombre IN ($1)", [req.params.category],
             function(err, result) {
            rowsAffected = result.rowCount;
        });

        // After all data is returned, close connection and return results
        query.on('end', function() {
            done();
            if (rowsAffected == 0){
                return res.status(404).json({'code': 0, 'message': 'Categoria Inexistente'});
            }
            return res.status(204).json({});
        });
    });
});

//INSERT categoria
router.post('/', function(req, res){
    if (req.body.category == undefined || req.body.category.name == undefined || req.body.category.description == undefined){
        return res.status(400).json({code: 0, message: 'Faltan parametros'});
    }
    // Grab data from http request
    var data = {nombre: req.body.category.name, descripcion: req.body.category.description};


    // Get a Postgres client from the connection pool
    pg.connect(connectionString, function(err, client, done) {
        // Handle connection errors
        if(err) {
            done();
            console.log(err);
            return res.status(500).json({code: 0, message: err});
        }
        // SQL Query > Insert Data
        var query = client.query('INSERT INTO categorias(nombre, descripcion) values($1, $2)',
            [data.nombre, data.descripcion]);

        query.on('error', function(err) {
            return res.status(500).json({code: 0, message: err});
        });

        // After all data is returned, close connection and return results
        query.on('end', function() {
            done();
            return res.status(201).json(req.body);
        });
    });
});


//Update Category
router.post('/:category', function(req, res){
    if (req.body.category == undefined || req.body.category.name == undefined || req.body.category.description == undefined){
        return res.status(400).json({code: 0, message: 'Faltan parametros'});
    }
    // Grab data from http request
    var category = req.params.category;
    var data = {nombre: req.body.category.name, descripcion: req.body.category.description};

    // Get a Postgres client from the connection pool
    pg.connect(connectionString, function(err, client, done) {
        // Handle connection errors
        if(err) {
            done();
            console.log(err);
            return res.status(500).json({code: 0, message: err});
        }
        var rowsAffected;
        // SQL Query > Insert Data
        var query = client.query('UPDATE categorias SET nombre=($1), descripcion=($2) WHERE nombre=($3)',
            [data.nombre, data.descripcion, category],
             function(err, result) {
            rowsAffected = result.rowCount;
        });



        // After all data is returned, close connection and return results
        query.on('end', function() {
            done();
            if (rowsAffected == 0) {return res.status(404).json({'code': 0, 'message': 'Categoria Inexistente'})}
            return res.status(201).json(req.body);
        });
    });

});

router.all('*', function(req, res, next){
  res.status(404);

  // respond with json
  if (req.accepts('json')) {
    res.send({code: 0, message: 'Not found'});
    return;
  }

  // default to plain-text. send()
  res.type('txt').send('Not found');
});


module.exports = router;