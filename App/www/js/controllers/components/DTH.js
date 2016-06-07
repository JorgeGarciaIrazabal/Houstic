/**
 * Created by Jorge on 23/05/2016.
 */
angular.module('houstic.controllers')
    .controller('DHTCtrl', function ($scope, $stateParams, $timeout, $interval, HubsApi) {
        $scope.getTemperature = function () {
            return $scope.component.value[0];
        };

        $scope.getHumidity = function () {
            return $scope.component.value[1];
        };
    });