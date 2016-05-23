/**
 * Created by Jorge on 23/05/2016.
 */
angular.module('houstic.controllers')
    .controller('HouseCtrl', function ($scope, $stateParams, $timeout, $interval, HubsApi) {
        console.log("house");
        var changeTimer = null,
            houseServer = HubsApi.HouseHub.server;
        $scope.house = $stateParams.house;
        $scope.house = {id: "574083ba97d0c72d7883c222", name: "myHouse"};
        $scope.components = [];

        $scope.onValueChanged = function (component) {
            if (changeTimer) {
                $timeout.cancel(changeTimer);
            }
            changeTimer = $timeout(function () {
                console.log(component.value);
                houseServer.componentWrite($scope.house.id, component.moduleId, component.name, parseInt(component.value))
                    .finally(function () {
                        changeTimer = null;
                    });
            }, 200)
        };

        HubsApi.HouseHub.server.getAllComponents($scope.house.id)
            .then(function (modules) {
                for (var module in modules) {
                    if (modules.hasOwnProperty(module)) {
                        for (var componentKey in modules[module]) {
                            if (modules[module].hasOwnProperty(componentKey)) {
                                var component = modules[module][componentKey];
                                component.name = componentKey;
                                component.icon = 'bonfire';
                                component.moduleId = module
                                $scope.components.push(component);
                            }
                        }
                    }
                }
            });

        $interval(function () {
            var sensors = $scope.components.filter(function (component) {
                return component.mode == 2;
            });
            sensors.forEach(function (sensor) {
                houseServer.componentRead($scope.house.id, sensor.moduleId, sensor.name)
                    .then(function (value) {
                        sensor.value = value;
                    })
            });
        }, 1000)
    });