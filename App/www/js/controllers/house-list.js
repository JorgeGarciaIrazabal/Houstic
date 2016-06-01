angular.module('houstic.controllers')
    .controller('HouseListCtrl', function ($scope, $state, HubsApi) {
        console.log("house_info list");
        $scope.houses = [];


        $scope.vewComponent = function (house_info) {
            $state.go("app.house", {house_info: house_info})
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