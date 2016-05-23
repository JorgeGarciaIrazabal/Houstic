angular.module('houstic.controllers')
    .controller('HouseListCtrl', function ($scope, $state, HubsApi) {
        console.log("house list");
        $scope.houses = [];


        $scope.vewComponent = function (house) {
            $state.go("app.house", {house: house})
        };

        HubsApi.HouseHub.server.listHouses()
            .then(function (houses) {
                $scope.houses = houses;
                $scope.houses.map(function (house) {
                    house.connectedIcon = house.connected ? "checkmark-circle-outline" : "close-circle";
                    house.name = house.name || "undefined";
                });
            });
    });