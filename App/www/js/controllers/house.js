/**
 * Created by Jorge on 23/05/2016.
 */
angular.module('houstic.controllers')
    .controller('HouseCtrl', function ($scope, $stateParams, $timeout, $interval, HubsApi) {
        var changeTimer = null;
        $scope.house_info = $stateParams.house_info;
        $scope.house_info = $scope.house_info || {id: "574083ba97d0c72d7883c222", name: "myHouse"};
        $scope.house = HubsApi.HouseHub.getClients($scope.house_info.id);
        $scope.components = [];

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

        $scope.house.getComponents()
            .then(function (modules) {
                modules.forEach(function (module) {
                    module.components.forEach(function (component, id) {
                        component.icon = 'bonfire';
                        component.moduleId = module.id;
                        component.index = id;
                        component.value = parseInt(component.value);
                        $scope.components.push(component);
                    })
                });
            });

        var interval = $interval(function () {
            var sensors = $scope.components.filter(function (component) {
                return component.mode == 2;
            });
            sensors.forEach(function (sensor) {
                $scope.house.componentRead(sensor.moduleId, sensor.index)
                    .then(function (value) {
                        sensor.value = value;
                    })
                    .catch(function (exception) {
                        if(exception.error !== undefined && exception.error.indexOf('No module with id')>=0){
                            $interval.cancel(interval);
                            alert("Module disconected");
                        }
                    })
            });
        }, 1000);

        $scope.$on("$destroy", function() {
            if (interval) {
                $interval.cancel(interval);
            }
        });
    });