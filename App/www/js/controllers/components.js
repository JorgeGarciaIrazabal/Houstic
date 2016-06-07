/**
 * Created by Jorge on 23/05/2016.
 */
angular.module('houstic.controllers')
    .controller('ComponentsCtrl', function ($scope, $stateParams, $timeout, $interval, HubsApi) {
        $scope.houseInfo = $stateParams.houseInfo || {id: "574083ba97d0c72d7883c222", name: "myHouse"};
        $scope.house = HubsApi.HouseHub.getClients($scope.houseInfo.id);
        $scope.module = $stateParams.module || {components: []};
        var interval = $interval(function () {
            var sensors = $scope.module.components.filter(function (component) {
                return [2, 6, 7].indexOf(component.mode) >= 0;
            });

            sensors.forEach(function (sensor) {
                $scope.house.componentRead($scope.module.id, sensor.index)
                    .then(function (value) {
                        sensor.value = value;
                    })
                    .catch(function (exception) {
                        if (exception.error !== undefined && exception.error.indexOf('No module with id') >= 0) {
                            $interval.cancel(interval);
                            alert("Module disconnected");
                        }
                    });
            });
        }, 3000);

        $scope.resetModule = function () {
            $scope.house.resetModule($scope.module.id)
                .catch(function (error) {
                    console.error(error);
                })
        };

        $scope.$on("$destroy", function () {
            if (interval) {
                $interval.cancel(interval);
            }
        });
    });