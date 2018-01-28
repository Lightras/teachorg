
app.controller('GroupsController', ['$scope', '$http', '$rootScope', function ($scope, $http, $rootScope) {

    $http({url: $rootScope.baseUrl + '/groupsdata'}).then(function (response) {
        $scope.allPupils = response.data;
        $scope.groupsObj = _.groupBy($scope.allPupils, 'group__name');
        $scope.groups = []

        for (prop in $scope.groupsObj) {
            $scope.groups.push({name: prop, pupils: $scope.groupsObj[prop]})
        }

        console.log($scope.groups);

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
                var csrf = $("[name='csrfmiddlewaretoken']").val();

                $.ajax({
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': csrf,
                        'group': $scope.newGroup.name,
                    },
                    success: function (data) {
                        console.log('success')
                    },
                    error:  function (error) {
                        console.log('error')
                    },
                })


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
            var csrf = $("[name='csrfmiddlewaretoken']").val();

            birthDate = new Date($scope.newPupil.dateBirth)
            var dd = birthDate.getUTCDate()
            var mm = birthDate.getUTCMonth()+1
            var yyyy = birthDate.getFullYear()
            console.log(dd+'/'+mm+'/'+yyyy)


                $.ajax({
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': csrf,
                        'first_name': $scope.newPupil.first_name,
                        'middle_name': $scope.newPupil.middle_name,
                        'last_name': $scope.newPupil.last_name,
                        'dateBirth': dd+'.'+mm+'.'+yyyy,
                        'group_name': $scope.newPupil.group__name,
                    },
                    success: function (data) {
                        console.log('success')
                    },
                    error:  function (error) {
                        console.log('error')
                    },
                })
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

        $scope.confirmEditPupil = function() {
            _.remove($scope.selectedGroup.pupils, {'first_name': $scope.editedPupilName});
            $scope.selectedGroup.pupils.push($scope.editedPupil);
            $('#edit-pupil-modal').modal('hide')

            var csrf = $("[name='csrfmiddlewaretoken']").val();

            birthDate = new Date($scope.editedPupil.dateBirth)
            var dd = birthDate.getUTCDate()
            var mm = birthDate.getUTCMonth()+1
            var yyyy = birthDate.getFullYear()
            console.log(dd+'/'+mm+'/'+yyyy)

                $.ajax({
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': csrf,
                        'first_name_edit': $scope.editedPupil.first_name,
                        'middle_name': $scope.editedPupil.middle_name,
                        'last_name': $scope.editedPupil.last_name,
                        'dateBirth': dd+'.'+mm+'.'+yyyy,
                        'group_name': $scope.editedPupil.group__name,
                        'pupil_id': $scope.editedPupil.id,
                    },
                    success: function (data) {
                        console.log('success')
                    },
                    error:  function (error) {
                        console.log('error')
                    },
                })

        }

        $scope.cancelEditPupil = function() {
            $scope.editedPupil = undefined;
            $('#edit-pupil-modal').modal('hide')
        }

        $scope.deletePupil = function() {
            console.log($scope.editedPupil);
            console.log($scope.selectedGroup.pupils);
            if ($scope.editedPupil.first_name) {
                var csrf = $("[name='csrfmiddlewaretoken']").val();
                $.ajax({
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': csrf,
                        'del_pupil': $scope.editedPupil.id,
                    },
                    success: function (data) {
                        console.log('success')
                    },
                    error:  function (error) {
                        console.log('error')
                    },
                })
                 _.remove($scope.selectedGroup.pupils, {'first_name': $scope.editedPupilName});
                $scope.editedPupilName = undefined;
                $scope.editedPupil = undefined;
                $('#edit-pupil-modal').modal('hide');

            }
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