/**
 * Created by Jorge on 23/05/2016.
 */
angular.module('houstic.constants')
    .constant('modules', {
        // Second parameter is 2 to tell server we are a mobile device
        BOILER: {
            templateUrl: "templates/modules/boiler.html",
            controller: "BoilerCtrl"
        }
    });