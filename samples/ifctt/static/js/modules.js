var ifctt = angular.module('ifctt', ['as.sortable', 'angular-loading-bar', 'ngSanitize'])
.config(['cfpLoadingBarProvider', function(cfpLoadingBarProvider) {
    cfpLoadingBarProvider.includeSpinner = false;
  }]);
