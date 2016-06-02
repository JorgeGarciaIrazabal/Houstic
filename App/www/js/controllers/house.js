angular.module('houstic.controllers')
    .controller('HouseCtrl', function ($scope, $state, $stateParams, HubsApi) {

        $scope.houseInfo = $stateParams.houseInfo || {id: "574083ba97d0c72d7883c222", name: "myHouse"};


        $scope.saveChanges = function () {
            HubsApi.HouseHub.server.update($scope.houseInfo)
                .then(function () {
                    $state.go("app.houseList", {}, {reload: true});
                });
        };

        $scope.rebootHouse = function () {
            alert("not implemented yet")
        };
    });