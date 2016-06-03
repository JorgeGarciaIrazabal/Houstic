/**
 * Created by Jorge on 03/06/2016.
 */
angular.module('houstic.directives', [])
    .directive('module', function ($state, modules) {
        return {
            restrict: 'E',
            scope: {
                module: '=',
                houseInfo: '=house'
            },
            link: function (scope){
                scope.module.components.forEach(function (component, i){
                    component.index = i;
                });
                scope.showComponents = function () {
                    $state.go("app.components", {houseInfo: scope.houseInfo, module: scope.module})
                };

                scope.templateUrl = modules[scope.module.type].templateUrl;
            },
            template: '<div ng-include="templateUrl" ></div>'
        }
    });