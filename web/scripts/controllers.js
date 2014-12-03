var controller = angular.module('comics')
  .controller('main' ['$scope',
    function($scope) {
      $scope.test = "Hello, World!";
    }]
  );
