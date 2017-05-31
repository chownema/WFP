/**
 * app.js
 * Author : Miguel Saavedra
 */
(function() {
angular.module('mainViewController', ['ngRoute'])

    // Run Configuration router
    .config(['$routeProvider', function ($routeProvider) {
        "use strict";
        // Register Constant Values
        var CNST = {
            // Jobs
            JOB_FORM : 'job-form.html',
            JOB_FORM_URL : '/job-form',
            JOB_VCTRL : 'JobViewController',
            JOB_VCTRL_ALIAS : 'JobCtrl',
            
            // Default
            DEFAULT_PANEL : 'content-pane.html'
        };

        // Router Logic on ng-view
        $routeProvider
            .when(CNST.JOB_FORM_URL, {
                templateUrl: CNST.JOB_FORM,
                controller: CNST.JOB_VCTRL,
                controllerAs: CNST.JOB_VCTRL_ALIAS,
                replace: true
            })
            // Default
            .otherwise({
                templateUrl: CNST.DEFAULT_PANEL,
                replace: true
            });
    }])
    
    // General View Controller
    .controller('viewController', ['$scope', function($scope) {
        // Do some general stuff
    }])

    // Job View controller
    .controller('JobViewController', ['$scope', function($scope) {
        $scope.dummyName = 'mr fong';
    }]);

})();