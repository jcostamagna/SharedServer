var app = angular.module('App', ['ngMaterial', 'ngMdIcons', 'md.data.table', 'ngRoute', 'ngAnimate']);

app.controller('AppController', ['$mdEditDialog', '$scope','$mdSidenav','$mdDialog','$http', '$timeout', function($mdEditDialog,$scope,$mdSidenav,$mdDialog,$http,$timeout) {

  $scope.selected = [];
  $scope.limitOptions = [5, 10, 15];

  $scope.options = {
    rowSelection: true,
    multiSelect: true,
    autoSelect: true,
    decapitate: false,
    largeEditDialog: false,
    boundaryLinks: false,
    limitSelect: true,
    pageSelect: true
  };

  $scope.query = {
    order: 'name',
    limit: 10,
    page: 1
  };

  $scope.putCategory = function (name,description) {
    console.log("putCategorias");
    var data = {category:{
                            name: name,
                            description: description
                            }
                };
    $http.post("/categories", JSON.stringify(data)).
        then(function (data, status, headers, config) { alert("success") },
             function (data, status, headers, config) { alert("error") });  
  }

  $scope.get = function (url) {
      $http.get(url)
      .success((data) => {
        $scope.items = data;
      })
      .error((error) => {
        console.log('Error: ' + error);
      });
  };


  $scope.editComment = function (event, item) {
    event.stopPropagation(); // in case autoselect is enabled
    
    var editDialog = {
      modelValue: item.description,
      placeholder: 'Agregar descripcion',
      save: function (input) {
        item.description = input.$modelValue;
      },
      targetEvent: event,
      title: 'Agregar descripcion',
      validators: {
        'md-maxlength': 50
      }
    };
  
    var promise;
    
    if($scope.options.largeEditDialog) {
      promise = $mdEditDialog.large(editDialog);
    } else {
      promise = $mdEditDialog.small(editDialog);
    }
    
    promise.then(function (ctrl) {
      var input = ctrl.getInput();
      
      input.$viewChangeListeners.push(function () {
        input.$setValidity('test', input.$modelValue !== 'test');
      });
    });
  };


  $scope.toggleLimitOptions = function () {
    $scope.limitOptions = $scope.limitOptions ? undefined : [5, 10, 15];
  };
  
  
  $scope.loadStuff = function (url) {
    $scope.url = url;
    $scope.promise = $timeout(function () {
       $scope.get($scope.url);
    }, 6000);
  }
  
  $scope.logItem = function (item) {
    console.log(item.name, 'seleccionado');
  };
  
  $scope.logOrder = function (order) {
    console.log('order: ', order);
  };
  
  $scope.logPagination = function (page, limit) {
    console.log('page: ', page);
    console.log('limit: ', limit);
  }

  /**
   * Hide or Show the 'left' sideNav area
   */
  $scope.toggleList = function toggleList() {
    $mdSidenav('left').toggle();
  }

  $scope.showAdd = function(ev) {
    $mdDialog.show({
      controller: DialogController,
      template: '<md-dialog aria-label="AddObject" ng-controller="AppController"> <md-content class="md-padding"> <form name="userForm"> <div layout="column" flex> <md-input-container flex><input ng-model="user.firstName" placeholder="Nombre"> </md-input-container> </div>                       <md-select aria-label="Categoria" ng-model="dessert.type" placeholder=""> <md-option ng-value="type" ng-repeat="type in getTypes()" style="background-color:rgb(190,190,220);">{{type}}</md-option></md-select>                       <md-input-container flex> <label>Descripcion</label> <textarea ng-model="user.biography" columns="1" md-maxlength="50"></textarea> </md-input-container> </form> </md-content> <div class="md-dialog-actions" layout="row"> <span flex></span> <md-button ng-click="answer(\'useful\')" class="md-primary"> Save </md-button> <md-button ng-click="answer(\'not useful\')"> Cancel </md-button> </div></md-dialog>',
      targetEvent: ev,
    })
    .then(function(answer) {
      $scope.alert = 'You said the information was "' + answer + '".';
    }, function() {
      $scope.alert = 'You cancelled the dialog.';
    });
  };


  function DialogController($scope, $mdDialog) {
    $scope.hide = function() {
      $mdDialog.hide();
    };
    $scope.cancel = function() {
      $mdDialog.cancel();
    };
    $scope.answer = function(answer) {
      $mdDialog.hide(answer);
    };
  };

}]);

app.animation('.slide-toggle', ['$animateCss', function($animateCss) {
    return {
        addClass: function(element, className, doneFn) {
            if (className == 'ng-hide') {
                var animator = $animateCss(element, {                    
                    to: {height: '0px', opacity: 0}
                });
                if (animator) {
                    return animator.start().finally(function() {
                        element[0].style.height = '';
                        doneFn();
                    });
                }
            }
            doneFn();
        },
        removeClass: function(element, className, doneFn) {
            if (className == 'ng-hide') {
                var height = element[0].offsetHeight;
                var animator = $animateCss(element, {
                    from: {height: '0px', opacity: 0},
                    to: {height: height + 'px', opacity: 1}
                });
                if (animator) {
                 return animator.start().finally(doneFn);
                }
            }
            doneFn();
        }
    };
}]);

app.config(function($routeProvider){
  //configuración y definición de las rutas
$routeProvider
            .when("/", {
                controller: "AppController",
                templateUrl: "vistas/home.html"
            })
            .when("/listado-job-positions", {
                controller: "AppController",
                templateUrl: "vistas/listadoJobPos.html"
            })
            .when("/listado-job-categories", {
                controller: "AppController",
                templateUrl: "vistas/CategoriasJobPos.html"
            })
            .when("/listado-skills", {
                controller: "AppController",
                templateUrl: "vistas/listadoSkills.html"
            })
            .when("/listado-skills-categories", {
                controller: "AppController",
                templateUrl: "vistas/CategoriasSkills.html"
            })
            .when("/listado-categories", {
                controller: "AppController",
                templateUrl: "vistas/Categorias.html"
            });
});