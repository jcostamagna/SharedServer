angular.module('App', ['ngMaterial'])

.controller('AppCtrl', function($scope) {

  $scope.Login = function(ev) {
    console.log("The button works!");
    console.log("Nombre de usuario: "+this.user.name);
    console.log("Clave: "+this.user.password);
  };

});