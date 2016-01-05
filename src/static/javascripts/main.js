'use strict'

angular.module('app',['ngRoute'])
	.value('endpoint','/_ah/api/services/v1')
	.service('UserService',['$http',function($http){			
		this.getUsers = function(){
			return $http.get('/_ah/api/services/v1/users')
		}
		
		this.getUser = function(id){
			return $http.get('/_ah/api/services/v1/users/'+id)
		}
	}])
	.config(function($routeProvider) {
		$routeProvider
		.when('/',{
			controller:'DashboardController as dashboard',
			templateUrl:'templates/dashboard.html'
		}).otherwise({
		      redirectTo:'/'
	    });
	})
	.controller('DashboardController',['$scope','UserService',function($scope, UserService){
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

