'use strict'

angular.module('app',[])
	.service('UserService',['$http',function($http){		
		this.getUsers = function(){
			console.log('FETCHING from ',this.endpoint, '/users')
			return $http.get('/_ah/api/services/v1/users')
		}
	}])
	.controller('userController',['$scope','UserService',function($scope, UserService){
		$scope.users = [];
        $scope.error = undefined;
        $scope.ready = false;
		
		UserService.getUsers()
			.success(function (users) {
	            $scope.users = users.data;
	            console.log($scope.users)
	            $scope.ready = true;
	        })
	        .error(function (error) {
	            $scope.error = error;
	            $scope.ready = true;
	        });
	}]);