/**
 * Created by Jorge on 23/05/2016.
 */
angular.module('houstic.controllers')
    .controller('ModuleListCtrl', function ($scope, $stateParams, $timeout, $interval, HubsApi) {
        $scope.houseInfo = $stateParams.houseInfo || {id: "574083ba97d0c72d7883c222", name: "myHouse"};
        $scope.house = HubsApi.HouseHub.getClients($scope.houseInfo.id);
        $scope.components = [];

        $scope.house.getModules()
            .then(function (modules) {
                $scope.modules = modules;
            })
            .catch(function (error) {
                console.error(error);
            });
    });