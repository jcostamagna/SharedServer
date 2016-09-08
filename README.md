# Taller de Programacion II - Shared Server </br>
 ![Build Status](https://travis-ci.org/nicomoccagatta/SharedServer.svg?branch=master) </br>

## Instrucciones para iniciar la webApp </br>
1) Para armar la imagen docker </br>
``$ cd WebApp``</br>
``$ docker build -t webapp . ``</br>
2) Para iniciar la webapp </br>
``$ docker run -p 49100:8080 webapp`` </br>
3) Ahora se puede acceder a la webapp accediendo al navegador e ingresando</br>
``http://localhost:49100`` </br>


### Instrucciones para correr el servidor NodeJS con Docker </br>
1) Para armar la imagen docker </br>
``$ docker build -t node-web-app . ``</br>
2) Para correr el servidor </br>
``$ docker run -p 49200:8080 node-web-app`` </br>
3) Ahora se puede acceder al servidor por consola con </br>
``$ curl -i localhost:49160`` </br>