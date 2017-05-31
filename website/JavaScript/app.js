(function() {
angular.module('mainViewController', ['ngRoute'])

    // Define some constants
    .constant('JOB_FORM', 'job-form.html')
    .constant('JOB_FORM_URL', '/job-form')
    .constant('JOB_VCTRL', 'JobViewController')

    // Run Configuration router
    .config(['$routeProvider', function (
        $routeProvider,
        JOB_FORM_URL,
        JOB_FORM,
        JOB_VCTRL) {
            "use strict";

            $routeProvider
            .when(JOB_FORM_URL, {
                templateUrl: JOB_FORM,
                controller: JOB_VCTRL,
                controllerAs: 'jobCtrl',
                replace: true
            })

            .otherwise({
                templateUrl: 'content-pane.html',
                replace: true
        });

    }])
    
    // General View Controller
    .controller('viewController', ['$scope', function($scope, JOB_FORM) {
        // Do some general stuff
    }])

    // Job View controller
    .controller('JobViewController', ['$scope', function($scope, JOB_FORM) {
        $scope.dummyName = 'mr fong';
    }]);

})();