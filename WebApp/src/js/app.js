angular.module('App',['ngMaterial'])

.controller('AppController', function($scope,$mdSidenav) {
  /**
   * Hide or Show the 'left' sideNav area
   */
  $scope.toggleList = function toggleList() {
    $mdSidenav('left').toggle();
  }

});