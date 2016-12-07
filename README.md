# Taller de Programacion II - Shared Server </br>
## Jobify - 2do cuatrimestre 2016 ![Build Status](https://travis-ci.org/jcostamagna/SharedServer.svg?branch=master) </br>

## Instrucciones para hacer el deploy local </br>
1) Para armar la imagen docker </br>
Hacemos cd sobre la carpeta donde descargamos el repositorio, luego hacemos </br>
``$ docker build -t ouruser/servernode . ``</br>
2) Para iniciar el server </br>
``$ docker run -p 8080:8080 ouruser/servernode`` </br>
3) Ahora se puede usar la webapp accediendo al navegador e ingresando</br>
``http://localhost:8080`` </br></br>

## Integrantes
#### Costamagna, Juan
#### Levinas, Alejandro
#### Moccagatta, Nicolas
#### Palma, Leandro