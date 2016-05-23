angular.module('houstic.factories', [])
    .factory('HubsApi', function (server) {
        console.log("creating hubsAPI");
        var api = new HubsAPI();
        api.connect(server.localDevelop, 2);
        return api
    });
