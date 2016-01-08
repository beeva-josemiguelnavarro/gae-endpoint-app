'use strict'

angular.module('app',['ngRoute'])
	.value('endpoint','/_ah/api/services/v1')
	.value('secret','Cp2MvDdxOlu7vYDgqWd-95rm')
	.service('UserService',['$http',function($http){
		var _endpoint = '/_ah/api/services/v1/';
		this.getUsers = function(){
			console.log(_endpoint+'users')
			return $http.get(_endpoint+'users')
		}
		
		this.getUser = function(id){
			console.log(_endpoint+'users/'+id)
			return $http.get(_endpoint+'users/'+id)
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

