/**
 * Created by Jorge on 23/05/2016.
 */
angular.module('houstic.controllers')
    .controller('BoilerCtrl', function ($scope, $stateParams, $timeout, HubsApi) {
        var changeTimer = null;
        $scope.house = HubsApi.HouseHub.getClients($scope.houseInfo.id);
        $scope.mainComponent = Enumerable.From($scope.module.components).First('$.name === "boiler"');

        $scope.onDigitalChanged = function (component) {
            if (changeTimer) {
                $timeout.cancel(changeTimer);
            }
            changeTimer = $timeout(function () {
                console.log(component.value);
                $scope.house.componentWrite($scope.module.id, component.index, component.value ? 1 : 0)
                    .catch(function (error) {
                        console.error(error);
                    })
                    .finally(function () {
                        changeTimer = null;
                    });
            }, 200);
        };
    });