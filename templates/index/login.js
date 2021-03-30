var app = angular.module("index", []);
app.controller("login", ["$scope", "service", function($scope, service) {
    $scope.result = "";
    $scope.my_submit = function() {
        console.log($scope.usr);
        console.log($scope.psw);
        service.do_save_info($scope.usr, $scope.psw, function(response){
            console.log(response);
            $scope.result = response.result;
        });
    };
}]);
app.service("service", ["$http", function($http) {
    this.do_save_info = function(username, password, callback) {
        $http({
            method: 'POST',
            url: '/do_save_info',
            data: {
                'username': username,
                'password': password
            },
            headers: {'Content-Type': undefined},
        }).success(function(response){
            callback(response);
        });
    };
}]);