# Taller de Programacion II - Shared Server
 ![Build Status](https://travis-ci.org/nicomoccagatta/SharedServer.svg?branch=master)

### Instrucciones para correr el servidor NodeJS con Docker
1) Para armar la imagen docker
$ docker build -t <nombre imagen>/node-web-app .
2) Para correr el servidor
$ docker run -p 49160:8080 -d <nombre imagen>/node-web-app
3) Ahora se puede acceder al servidor por consola con
$ curl -i localhost:49160