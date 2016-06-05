/**
 * Created by Jorge on 03/06/2016.
 */
angular.module('houstic.directives')
    .directive('component', function ($state, $ionicViewSwitcher, components) {
        return {
            restrict: 'E',
            scope: {
                component: '=',
                house: '=',
                module: '='
            },
            link: function (scope) {
                scope.templateUrl = components[scope.component.mode].templateUrl;
            },
            template: '<div ng-include="templateUrl"></div>'
        }
    });