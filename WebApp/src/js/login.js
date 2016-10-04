var app = angular.module('Login', ['ngMaterial'])

.controller('LoginCtrl', function($scope) {
    $scope.Login = function(ev) {
    console.log("Nombre de usuario: "+this.user.name);
    console.log("Clave: "+this.user.password);

    if (this.user.name=="admin" && this.user.password=="admin") {
    	console.log("CREDENCIALES CORRECTAS");
    	window.location = "src/app.html";
    }
    else {
    	console.log("CREDENCIALES INCORRECTAS");
    }
  };

});

app.directive('myEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if(event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.myEnter);
                });
            }
        });
    };
});