angular.module('houstic.factories', [])
    .factory('HubsApi', function ($q, server) {
        console.log("creating hubsAPI");
        var api = new HubsAPI(5000, undefined, $q);
        api.onMessageError = function (error) {
          console.error(error);
        };
        api.connect(server.localDevelop, 2);
        return api
    });
