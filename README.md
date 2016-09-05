# Taller de Programacion II - Shared Server </br>
 ![Build Status](https://travis-ci.org/nicomoccagatta/SharedServer.svg?branch=master) </br>

### Instrucciones para correr el servidor NodeJS con Docker </br>
1) Para armar la imagen docker </br>
``$ docker build -t nombre-imagen/node-web-app . ``</br>
2) Para correr el servidor </br>
``$ docker run -p 49160:8080 -d nombre-imagen/node-web-app`` </br>
3) Ahora se puede acceder al servidor por consola con </br>
``$ curl -i localhost:49160`` </br>