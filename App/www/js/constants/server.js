/**
 * Created by Jorge on 23/05/2016.
 */
angular.module('houstic.constants', [])
    .constant('server', {
        // Second parameter is 2 to tell server we are a mobile device
        externalRelease: 'ws://198.100.155.30:9517/2',
        externalDevelop: 'ws://198.100.155.30:9518/2',
        localRelease: 'ws://192.168.1.6:9517/2',
        localDevelop: 'ws://192.168.1.6:9518/2'
    });