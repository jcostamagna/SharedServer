/**
 * Created by juan on 16/11/16.
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

/*
var query = client.query(
    'DROP TABLE IF EXISTS job_positions');
query.on('end', () => { client.end(); });
*/

query = client.query(
    'CREATE TABLE IF NOT EXISTS job_positions(nombre VARCHAR(40), descripcion VARCHAR(140),' +
    ' categoria VARCHAR(40) REFERENCES categorias(nombre) on DELETE CASCADE, PRIMARY KEY (nombre, categoria))');
query.on('end', () => { client.end(); });


//Funcion de testeo para limpiar la tabla de job_positions
router.get('/test', function(req, res) {
    pg.connect(connectionString, function(err, client, done) {
        // Handle connection errors
        if(err) {
            done();
            console.log(err);
            return res.status(404).json({code: 0, message: err});
        }

        // SQL Query > DELETE Data
        var query = client.query('DELETE FROM job_positions');

        // After all data is returned, close connection and return results
        query.on('end', function() {
            done();
            return res.status(201).json([]);
        });
    });

});

//GET job_positions
router.get('/', function(req, res) {
    var rows = {};
    rows['job_positions'] = [];
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
        var query = client.query('SELECT * FROM job_positions');
        // Stream results back one row at a time
        query.on('row', function(row) {
            registro = {};
            registro['name'] = row.nombre;
            registro['description'] = row.descripcion;
            registro['category'] = row.categoria;
            rows['job_positions'].push(registro);
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

//GET job_position By category
router.get('/categories/:category', function(req, res) {
    var rows = {};
    rows['job_positions'] = [];
    rows['metadata'] = {};
    var registro = {};
    var categoria = req.params.category;

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
        var query = client.query('SELECT * FROM job_positions WHERE categoria IN ($1)', [categoria]);
        // Stream results back one row at a time
        query.on('row', function(row) {
            registro = {};
            registro['name'] = row.nombre;
            registro['description'] = row.descripcion;
            registro['category'] = row.categoria;
            rows['job_positions'].push(registro);
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

//DELETE job_position
router.delete('/categories/:category/:job_position', function (req, res) {
    if (req.params.category == undefined || req.params.job_position == undefined ){
        return res.status(400).json({code: 0, message: 'Faltan parametros'});
    }
    pg.connect(connectionString, function(err, client, done) {
        // Handle connection errors
        if(err) {
            done();
            console.log(err);
            return res.status(404).json({success: false, data: err, context: '/delete'});
        }
        var rowsAffected;
        // SQL Query > DELETE Data
        var query = client.query("DELETE FROM job_positions WHERE nombre=($1) AND categoria=($2)",
            [req.params.job_position, req.params.category], function(err, result) {
            rowsAffected = result.rowCount;
        });


        // After all data is returned, close connection and return results
        query.on('end', function(result) {
            done();
            if (rowsAffected == 0){
                return res.status(404).json({'code': 0, 'message': 'Categoria Inexistente'});
            }
            return res.status(204).json({});
        });
    });
});

//INSERT job_position
router.post('/categories/:category', function(req, res){
    if (req.body.job_position == undefined || req.body.job_position.name == undefined || req.body.job_position.description == undefined){
        return res.status(400).json({code: 0, message: 'Faltan parametros'});
    }
    // Grab data from http request
    var data = {nombre: req.body.job_position.name, descripcion: req.body.job_position.description, categoria: req.params.category};


    // Get a Postgres client from the connection pool
    pg.connect(connectionString, function(err, client, done) {
        // Handle connection errors
        if(err) {
            done();
            console.log(err);
            return res.status(500).json({code: 0, message: err});
        }
        // SQL Query > Insert Data
        var query = client.query('INSERT INTO job_positions(nombre, descripcion, categoria) values($1, $2, $3)',
            [data.nombre, data.descripcion, data.categoria]);

        query.on('error', function(err) {
            return res.status(404).json({'code': 0, 'message': 'Categoria Inexistente'});
        });

        // After all data is returned, close connection and return results
        query.on('end', function() {
            done();
            return res.status(201).json({'job_position': {'name': data.nombre, 'description': data.descripcion, 'category': data.categoria}});
        });
    });
});


//Update job_position
router.put('/categories/:category/:job_position', function(req, res){
    if (req.body.job_position == undefined || req.body.job_position.name == undefined || req.body.job_position.description == undefined){
        return res.status(400).json({code: 0, message: 'Faltan parametros'});
    }
    // Grab data from http request
    var oldCategory = req.params.category;
    var job_position = req.params.job_position;
    var data = {nombre: req.body.job_position.name, newCategory: req.body.job_position.category, descripcion: req.body.job_position.description};

    // Get a Postgres client from the connection pool
    pg.connect(connectionString, function(err, client, done) {
        // Handle connection errors
        if(err) {
            done();
            console.log(err);
            return res.status(500).json({code: 0, message: err});
        }

        // SQL Query > Insert Data
        var query = client.query('UPDATE job_positions SET categoria=($2),descripcion=($4) WHERE nombre=($1) AND categoria=($3)',
            [data.nombre, data.newCategory, oldCategory, data.descripcion])

        query.on('error', function(err) {
            return res.status(404).json({'code': 0, 'message': 'Categoria Inexistente'});
        });


        // After all data is returned, close connection and return results
        query.on('end', function() {
            done();
            return res.status(201).json(req.body);
        });
    });

});


module.exports = router;
