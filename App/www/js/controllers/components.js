/**
 * Created by Jorge on 23/05/2016.
 */
angular.module('houstic.controllers')
    .controller('ComponentsCtrl', function ($scope, $stateParams, $timeout, $interval, HubsApi) {
        var changeTimer = null;
        $scope.houseInfo = $stateParams.houseInfo || {id: "574083ba97d0c72d7883c222", name: "myHouse"};
        $scope.house = HubsApi.HouseHub.getClients($scope.houseInfo.id);
        $scope.module = $stateParams.module || {components: []};

        $scope.onRangeChanged = function (component) {
            if (changeTimer) {
                $timeout.cancel(changeTimer);
            }
            changeTimer = $timeout(function () {
                console.log(component.value);
                $scope.house.componentWrite(component.moduleId, component.index, parseInt(component.value))
                    .finally(function () {
                        changeTimer = null;
                    });
            }, 200)
        };

        $scope.onDigitalChanged = function (component) {
            if (changeTimer) {
                $timeout.cancel(changeTimer);
            }
            changeTimer = $timeout(function () {
                console.log(component.value);
                $scope.house.componentWrite(component.moduleId, component.index, component.value ? 1 : 0)
                    .finally(function () {
                        changeTimer = null;
                    });
            }, 200);
        };

        var interval = $interval(function () {
            var sensors = $scope.module.components.filter(function (component) {
                return component.mode == 2;
            });
            sensors.forEach(function (sensor) {
                $scope.house.componentRead($scope.module.id, sensor.index)
                    .then(function (value) {
                        sensor.value = value;
                    })
                    .catch(function (exception) {
                        if (exception.error !== undefined && exception.error.indexOf('No module with id') >= 0) {
                            $interval.cancel(interval);
                            alert("Module disconected");
                        }
                    })
            });
        }, 1000);

        $scope.$on("$destroy", function () {
            if (interval) {
                $interval.cancel(interval);
            }
        });
    });