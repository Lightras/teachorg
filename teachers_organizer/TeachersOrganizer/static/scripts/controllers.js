
app.controller('GroupsController', ['$scope', '$http', function ($scope, $http) {

    $http({url:'http://127.0.0.1:8000/groupsdata'}).then(function (response) {
        console.log("data: ", response.data);
        $scope.groups = response.data;
    }, function (error) {
        console.log("error: ", error);
    })

}]);

app.controller('LoginController', ['$scope', '$rootScope', function ($scope, $rootScope) {
}])

app.controller('NavbarController', ['$scope', '$location', function($scope, $location){
    console.log('hey NavbarController')
    var url = $location.url
    console.log(url)
}])