var server = require("./Server/server");
var router = require("./Controllers/router");
var requestHandlers = require("./Controllers/requestHandlers");

var handle = {}
handle["/"] = requestHandlers.iniciar;
handle["/iniciar"] = requestHandlers.iniciar;
handle["/subir"] = requestHandlers.subir;

server.iniciar(router.route, handle);
