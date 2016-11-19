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

  $scope.get = function (url) {
      $http.get(url)
      .success((data) => {
        $scope.items = data;

      })
      .error((error) => {
        alert("Error obteniendo datos")
      });
  };

  $scope.refreshCategories = function () {
      $http.get('/categories')
      .success((data) => {
        $scope.categories = data.categories;
      })
      .error((error) => {
        alert("Error obteniendo datos")
      });
  }

  $scope.getCategories = function () {
    return $scope.categories;
  }

  $scope.deleteCategory = function (url) {
      for (var i = $scope.selected.length - 1; i >= 0; i--) {
        $http.delete(url+$scope.selected[i].name);
      }
      $scope.selected = [];
      $scope.loadStuff(url);
  }

  $scope.delete = function (url, itemName) {
      for (var i = $scope.selected.length - 1; i >= 0; i--) {
        $http.delete(url+$scope.selected[i].category+'/'+$scope.selected[i].name);
      }
      $scope.selected = [];
      $scope.loadStuff('/'+itemName);
  }

  $scope.editCategoryComment = function (event, item, url) {
    event.stopPropagation(); // in case autoselect is enabled
    
    var editDialog = {
      modelValue: item.description,
      placeholder: 'Agregar descripcion',
      save: function (input) {
        item.description = input.$modelValue;
        var data = {category:{
                                name: item.name,
                                description: input.$modelValue
                                }
                    };
        $http.post(url+item.name,JSON.stringify(data));
        $scope.loadStuff(url);
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

  $scope.editComment = function (event, item, url, itemName) {
    event.stopPropagation(); // in case autoselect is enabled

    var editDialog = {
      modelValue: item.description,
      placeholder: 'Agregar descripcion',
      save: function (input) {
        if (itemName == 'job_position') {
          var data = {job_position:{
                                    name: item.name,
                                    category: item.category,
                                    description: input.$modelValue
                                }
                     };
        } else if (itemName == 'skill') {
          var data = {skill:{
                                    name: item.name,
                                    category: item.category,
                                    description: input.$modelValue
                                }
                     };
        } else {
              alert("Error modificando comentario.");
              return;
        }
        item.description = input.$modelValue;
        $http.put(url+item.category+'/'+item.name,JSON.stringify(data));
        $scope.loadStuff('/'+itemName+'s');
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
    $scope.refreshCategories();
    $scope.promise = $timeout(function () {
       $scope.get(url);
    },1000);
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

  $scope.showAddCategory = function(ev) {
    $scope.get('/categories');
    $mdDialog.show({
      targetEvent: ev,
      template: '<md-dialog aria-label="AddObject" ng-controller="AppController">'+
                '     <md-content class="md-padding">'+
                '       <form name="userForm">'+
                '          <div layout="column" flex>'+
                '             <md-input-container flex>'+
                '               <input ng-model="user.firstName" placeholder="Nombre"> '+
                '             </md-input-container> '+
                '          </div>'+
                ''+
                ''+
                '          <md-input-container flex>'+
                '             <label>Descripcion</label> '+
                '             <textarea ng-model="user.description" columns="1" md-maxlength="50">'+
                '             </textarea> '+
                '           </md-input-container>'+
                '        </form>'+
                '     </md-content>'+
                ' <div class="md-dialog-actions" layout="row">'+
                '   <span flex></span>'+
                '   <md-button ng-click="add(user.firstName,user.description)" class="md-primary"> Guardar </md-button>'+
                '   <md-button ng-click="answer(\'CANCEL\')"> Cancelar </md-button> </div></md-dialog>',
      controller: DialogController
    })
    .then(function(answer) {
      if (answer == 'OK') {
        $scope.loadStuff('/categories');
      }
    }, function() {
    });

    function DialogController($scope, $mdDialog, $http) {
      
      $scope.hide = function() {
        $mdDialog.hide();
      };

      $scope.cancel = function() {
        $mdDialog.cancel();
      };

      $scope.answer = function(answer) {
        $mdDialog.hide(answer);
      };

      $scope.add = function(name,description) {
        var data = {category:{
                                name: name,
                                description: description
                                }
                    };
        $http.post("/categories", JSON.stringify(data));
            
        $mdDialog.hide("OK");
      }
    };

  };

  $scope.showAdd = function(ev, itemName) {
    $scope.refreshCategories();
    $scope.itemName = itemName;

    $mdDialog.show({
      targetEvent: ev,
      template: '<md-dialog aria-label="AddObject" ng-controller="AppController">'+
                '     <md-content class="md-padding">'+
                '       <form name="userForm">'+
                '          <div layout="column" flex>'+
                '             <md-input-container flex>'+
                '               <input ng-model="user.firstName" placeholder="Nombre"> '+
                '             </md-input-container> '+
                '          </div>'+
                ''+
                '          <md-select aria-label="Categoria" ng-model="category.name" placeholder="">'+
                '              <md-option ng-value=category.name ng-repeat="category in categories" style="background-color:rgb(190,190,220);">'+
                '                   {{category.name}}'+
                '               </md-option>'+
                '          </md-select>'+
                ''+
                '          <md-input-container flex>'+
                '             <label>Descripcion</label> '+
                '             <textarea ng-model="user.description" columns="1" md-maxlength="50">'+
                '             </textarea> '+
                '           </md-input-container>'+
                '        </form>'+
                '     </md-content>'+
                ' <div class="md-dialog-actions" layout="row">'+
                '   <span flex></span>'+
                '   <md-button ng-click="add(user.firstName,user.description,category.name)" class="md-primary"> Guardar </md-button>'+
                '   <md-button ng-click="answer(\'CANCEL\')"> Cancelar </md-button> </div></md-dialog>',
      locals: {
        categories: $scope.categories,
        itemName: $scope.itemName
      },
      controller: DialogController
    })
    .then(function(answer) {
      if (answer == 'OK') {
        $scope.loadStuff('/'+$scope.itemName+'s');
      }
    }, function() {
    });

    function DialogController($scope, $mdDialog, categories, itemName, $http) {
      $scope.categories = categories;
      $scope.itemName = itemName;
      
      $scope.hide = function() {
        $mdDialog.hide();
      };

      $scope.cancel = function() {
        $mdDialog.cancel();
      };

      $scope.answer = function(answer) {
        $mdDialog.hide(answer);
      };

      $scope.add = function(name,description,category) {
        if ($scope.itemName == 'skill') {
          var data = {skill:{
                                  name: name,
                                  description: description
                                  }
                      };
        } else if ($scope.itemName == 'job_position') {
          var data = {job_position:{
                                  name: name,
                                  description: description
                                  }
                      };
        } else {
          alert("Error agregando item.");
          return;
        }
        $http.post('/'+$scope.itemName+'s/categories/'+category, JSON.stringify(data)).
            then(function (data, status, headers, config) {},
                 function (data, status, headers, config) { alert("Error agregando item.") });  
            
        $mdDialog.hide("OK");
      }
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