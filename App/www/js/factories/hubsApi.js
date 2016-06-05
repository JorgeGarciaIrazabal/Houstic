angular.module('houstic.factories', [])
    .factory('HubsApi', function ($q, server) {
        var api = new HubsAPI(5000, undefined, $q);
        api.onMessageError = function (error) {
            console.error(error);
        };
        api.connect(server.localDevelop, 2);

        window.addEventListener('unhandledrejection', function(event) {
            console.error('Unhandled rejection (promise: ', event.promise, ', reason: ', event.reason, ').');
        });
        return api
    });
