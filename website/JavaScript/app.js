/**
 * app.js
 * Author : Miguel Saavedra
 */


(function () {
    angular.module('mainViewController', ['ngRoute', 'chart.js'])

    // Run Configuration router
        .config(['$routeProvider', function ($routeProvider) {
            "use strict";
            // Register Constant Values
            var CNST = {
                // Jobs
                JOB_FORM: 'job-view.html',
                JOB_FORM_URL: '/job-view',
                JOB_VCTRL: 'JobViewController',
                JOB_VCTRL_ALIAS: 'JobCtrl',
                // Default
                DEFAULT_PANEL_URL: 'content-pane.html'
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
                    templateUrl: CNST.DEFAULT_PANEL_URL,
                    replace: true
                });
        }])

        // General View Controller
        .controller('viewController', ['$scope', function ($scope) {
            // Do some general stuff
        }])

        // Job View controller
        .controller('JobViewController', ['$scope', '$http', function ($scope, $http) {
			
        }])

        // General View Controller
        .controller('lineCtrl', ['$scope', function ($scope) {
            // Do some general stuff
            $scope.labels = ["January", "February", "March", "April"];
            $scope.series = ['Series A', 'Series B'];
            $scope.data = [
                [65, 59, 80, 81],
                [28, 48, 40, 19]
            ];
            $scope.onClick = function (points, evt) {
                console.log(points, evt);
            };
            $scope.datasetOverride = [{yAxisID: 'y-axis-1'}, {yAxisID: 'y-axis-2'}];
            $scope.options = {
                scales: {
                    yAxes: [
                        {
                            id: 'y-axis-1',
                            type: 'linear',
                            display: true,
                            position: 'left'
                        },
                        {
                            id: 'y-axis-2',
                            type: 'linear',
                            display: true,
                            position: 'right'
                        }
                    ]
                }
            };
        }])

        .controller("barCtrl",
		  function ($scope) {
			$scope.labels = ['2006', '2007', '2008', '2009', '2010', '2011', '2012'];
			$scope.series = ['Series A', 'Series B'];

			$scope.data = [
			  [65, 59, 80, 81, 56, 55, 40],
			  [28, 48, 40, 19, 86, 27, 90]
			];
		})
		
		.controller("pieCtrl", function ($scope) {
		  $scope.labels = ["Download Sales", "In-Store Sales", "Mail-Order Sales"];
		  $scope.data = [300, 500, 100];
		});

})();

