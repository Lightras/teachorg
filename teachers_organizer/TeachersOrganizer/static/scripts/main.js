var app = angular.module('TeachOrg', []);

angular.element(document).ready(function () {
    angular.bootstrap(document, ['TeachOrg']);
});

app.run(['$rootScope', function($rootScope) {
    $rootScope.baseUrl = 'http://127.0.0.1:8000';
}])