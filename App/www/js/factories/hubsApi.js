angular.module('houstic.factories', [])
    .factory('HubsApi', function () {
        console.log("creating hubsAPI");
        var api = new HubsAPI();
        var MOBILE = 2; // defined in global server, HOUSE is 1
        api.connect('ws://127.0.0.1:9517/' + MOBILE, 2);
        return api
    });
