
app.controller('GroupsController', ['$scope', '$http', '$rootScope', function ($scope, $http, $rootScope) {

    $http({url: $rootScope.baseUrl + '/groupsdata'}).then(function (response) {
        $scope.allPupils = response.data;
        $scope.groupsObj = _.groupBy($scope.allPupils, 'group__name');
        $scope.groups = []

        for (prop in $scope.groupsObj) {
            $scope.groups.push({name: prop, pupils: $scope.groupsObj[prop]})
        }

        $scope.selectGroup = function(groupName) {
            $scope.selectedGroup = _.find($scope.groups, {'name': groupName})
        }

        $scope.addGroup = function() {
            $scope.newGroup = {pupils:[]}
            $('#add-group-modal').modal()
        }

        $scope.confirmAddGroup = function() {
            if ($scope.newGroup.name) {
                $scope.groups.push($scope.newGroup);
                $scope.selectedGroup = $scope.newGroup;
                $('#add-group-modal').modal('hide')
            } else {
                $scope.showInfoMessage = true;
            }
        }

        $scope.cancelAddGroup = function() {
            $scope.newGroup = {pupils:[]};
            $('#add-group-modal').modal('hide')
        }

        $scope.editGroup = function(group) {
            $scope.editedGroupName = group.name;
            $scope.editedGroup = angular.copy(group);
            $('#edit-group-modal').modal()
        }

        $scope.deleteGroup = function() {
            if ($scope.editedGroup.name) {
                _.remove($scope.groups, {name: $scope.editedGroup.name});
                $scope.editedGroupName = undefined;
                $('#edit-group-modal').modal('hide');
            }
        }

        $scope.confirmEditGroup = function() {
            if ($scope.editedGroup.name) {
                _.find($scope.groups, {name: $scope.editedGroupName}).name = $scope.editedGroup.name;
                $scope.editedGroupName = undefined;
                $('#edit-group-modal').modal('hide');
            }
        }

        $scope.cancelEditGroup = function() {
            $scope.editedGroupName = undefined;
            $('#edit-group-modal').modal('hide');
        }

        $scope.showAddPupilForm = function() {
            $scope.newPupil = {group__name: $scope.selectedGroup.name}
            $('#add-pupil-modal').modal();
        }

        $scope.addPupil = function() {
            if ($scope.addPupilForm.$valid) {
                $scope.selectedGroup.pupils.push($scope.newPupil);
                $('#add-pupil-modal').modal('hide')
            }
        }

        $scope.cancelAddPupil = function() {
            $scope.newPupil = undefined;
            $('#add-pupil-modal').modal('hide')
        }

        $scope.showEditPupilModal = function(pupil) {
            $scope.editedPupilName = pupil.first_name;
            $scope.editedPupil = angular.copy(pupil)
            $('#edit-pupil-modal').modal()
        }


    }, function (error) {
        console.log("error: ", error);
    })

}]);

app.controller('LoginController', ['$scope', '$rootScope', function ($scope, $rootScope) {
}])

app.controller('NavbarController', ['$scope', '$location', function($scope, $location){
    var url = window.location.pathname;

   if(url == '/login/' || url == '/registration/') {
        $scope.hideNavbar = true;
   } else {
        $scope.hideNavbar = false;
   }
}])