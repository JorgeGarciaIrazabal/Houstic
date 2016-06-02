angular.module('houstic.controllers')
    .controller('HouseListCtrl', function ($scope, $state, HubsApi) {
        console.log("houseInfo list");
        $scope.houses = [];


        $scope.vewComponent = function (houseInfo) {
            if(houseInfo.connected){
                $state.go("app.moduleList", {houseInfo: houseInfo})
            }
        };

        $scope.viewHouseDetails = function (houseInfo) {
            $state.go("app.house", {houseInfo: houseInfo})
        };

        $scope.$on('$ionicView.beforeEnter', function () {
            HubsApi.HouseHub.server.listHouses()
                .then(function (houses) {
                    $scope.houses = houses;
                    $scope.houses.map(function (house) {
                        house.connectedIcon = house.connected ? "checkmark-circle-outline" : "close-circle";
                        house.formattedName = house.name || "undefined";
                    });
                });
        })
    });