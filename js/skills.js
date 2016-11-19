/**
 * Created by juan on 10/11/16.
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
    'DROP TABLE IF EXISTS skills');
query.on('end', () => { client.end(); });
*/

query = client.query(
    'CREATE TABLE IF NOT EXISTS skills(nombre VARCHAR(40), descripcion VARCHAR(140),' +
    ' categoria VARCHAR(40) REFERENCES categorias(nombre) on DELETE CASCADE, PRIMARY KEY (nombre, categoria))');
query.on('end', () => { client.end(); });


//Funcion de testeo para limpiar la tabla de skills
router.get('/test', function(req, res) {
    pg.connect(connectionString, function(err, client, done) {
        // Handle connection errors
        if(err) {
            done();
            console.log(err);
            return res.status(404).json({code: 0, message: err});
        }

        // SQL Query > DELETE Data
        var query = client.query('DELETE FROM skills');

        // After all data is returned, close connection and return results
        query.on('end', function() {
            done();
            return res.status(201).json([]);
        });
    });

});

//GET skill
router.get('/', function(req, res) {
    var rows = {};
    rows['skills'] = [];
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
        var query = client.query('SELECT * FROM skills');
        // Stream results back one row at a time
        query.on('row', function(row) {
            registro = {};
            registro['name'] = row.nombre;
            registro['description'] = row.descripcion;
            registro['category'] = row.categoria;
            rows['skills'].push(registro);
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

//GET skill By category
router.get('/categories/:category', function(req, res) {
    var rows = {};
    rows['skills'] = [];
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
        var query = client.query('SELECT * FROM skills WHERE categoria IN ($1)', [categoria]);
        // Stream results back one row at a time
        query.on('row', function(row) {
            registro = {};
            registro['name'] = row.nombre;
            registro['description'] = row.descripcion;
            registro['category'] = row.categoria;
            rows['skills'].push(registro);
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

//DELETE skill
router.delete('/categories/:category/:skill', function (req, res) {
    if (req.params.category == undefined || req.params.skill == undefined ){
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
        var query = client.query("DELETE FROM skills WHERE nombre=($1) AND categoria=($2)",
            [req.params.skill, req.params.category], function(err, result) {
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

//INSERT skill
router.post('/categories/:category', function(req, res){
    if (req.body.skill == undefined || req.body.skill.name == undefined || req.body.skill.description == undefined){
        return res.status(400).json({code: 0, message: 'Faltan parametros'});
    }
    // Grab data from http request
    var data = {nombre: req.body.skill.name, descripcion: req.body.skill.description, categoria: req.params.category};


    // Get a Postgres client from the connection pool
    pg.connect(connectionString, function(err, client, done) {
        // Handle connection errors
        if(err) {
            done();
            console.log(err);
            return res.status(500).json({code: 0, message: err});
        }
        // SQL Query > Insert Data
        var query = client.query('INSERT INTO skills(nombre, descripcion, categoria) values($1, $2, $3)',
            [data.nombre, data.descripcion, data.categoria]);

        query.on('error', function(err) {
            return res.status(404).json({'code': 0, 'message': 'Categoria Inexistente'});
        });

        // After all data is returned, close connection and return results
        query.on('end', function() {
            done();
            return res.status(201).json({'skill': {'name': data.nombre, 'description': data.descripcion, 'category': data.categoria}});
        });
    });
});


//Update Skill
router.put('/categories/:category/:skill', function(req, res){
    if (req.body.skill == undefined || req.body.skill.name == undefined || req.body.skill.description == undefined){
        return res.status(400).json({code: 0, message: 'Faltan parametros'});
    }
    // Grab data from http request
    var oldCategory = req.params.category;
    var skill = req.params.skill;
    var data = {nombre: req.body.skill.name, newCategory: req.body.skill.category, descripcion: req.body.skill.description};

    // Get a Postgres client from the connection pool
    pg.connect(connectionString, function(err, client, done) {
        // Handle connection errors
        if(err) {
            done();
            console.log(err);
            return res.status(500).json({code: 0, message: err});
        }

        // SQL Query > Insert Data
        var query = client.query('UPDATE skills SET categoria=($2),descripcion=($4) WHERE nombre=($1) AND categoria=($3)',
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
