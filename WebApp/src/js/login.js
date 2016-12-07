var app = angular.module('Login', ['ngMaterial'])

.controller('LoginCtrl', function($scope) {
    $scope.Login = function(ev) {
        if (this.user.name=="admin" && this.user.password=="admin") {
        	window.location = "src/app.html";
        }
        else {
            alert("CREDENCIALES INCORRECTAS");
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