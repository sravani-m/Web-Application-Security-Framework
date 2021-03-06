   �         Bhttp://testhtml5.vulnweb.com/static/app/controllers/controllers.js     %� ��      %{g06              �      
     H T T P / 1 . 1   2 0 0      Content-Type   'application/x-javascript; charset=utf-8   Content-Length   2778   Server   nginx/1.4.1   Date   Sat, 24 Jan 1970 03:09:39 GMT   Last-Modified   Fri, 10 May 2013 10:11:54 GMT   Etag   "518cc7ea-a16"   Expires   Mon, 23 Feb 1970 03:09:39 GMT   Cache-Control   max-age=2592000                 // Injected by Arachni::Browser::Javascript
                _arachni_js_namespaceTaintTracer.update_tracers();
                _arachni_js_namespaceDOMMonitor.update_trackers();
﻿app.controller('PopularItemsController', function ($scope, $routeParams, itemsService) {
    $scope.ctrlName = "popular";

    $scope.showLoader = showLoader;
    $scope.hideLoader = hideLoader;
    $scope.showLoader();

    $scope.page = ($routeParams.page) ? parseInt($routeParams.page) : 0;
    $scope.pageStr = ($routeParams.page) ? $routeParams.page : "0";

    $scope.filter = ($routeParams.filter) ? $routeParams.filter : "";

    if ($scope.filter) {
        itemsService.getArchiveItems(function(data, status) {

            if (status < 200 || status >= 300)
                return;

            $scope.items = data;
            $scope.hideLoader();
        });
    }
    else {
        itemsService.getPopularItems($scope.page, function(data, status) {

            if (status < 200 || status >= 300)
                return;

            $scope.items = data;
            $scope.hideLoader();
        });
    }

    $scope.like = function(id) {
        itemsService.like(id, function(data, status) {
            if (status < 200 || status >= 300)
                return;

            $scope.response = data;
        });
    };

});

app.controller('LatestItemsController', function ($scope, $routeParams, itemsService) {
    $scope.ctrlName = "latest";

    $scope.showLoader = showLoader;
    $scope.hideLoader = hideLoader;
    $scope.showLoader();

    $scope.page = ($routeParams.page) ? parseInt($routeParams.page) : 0;
    $scope.pageStr = ($routeParams.page) ? $routeParams.page : "0";

    $scope.filter = ($routeParams.filter) ? $routeParams.filter : "";


    itemsService.getLatestItems($scope.page, function(data, status) {

        if (status < 200 || status >= 300)
            return;

        $scope.items = data;
        $scope.hideLoader();
    });

    $scope.like = function(id) {
        itemsService.like(id, function(data, status) {
            if (status < 200 || status >= 300)
                return;

            $scope.response = data;
        });
    };
});

app.controller('ArchiveItemsController', function ($scope, $routeParams, itemsService) {
    $scope.ctrlName = "archive";

    $scope.showLoader = showLoader;
    $scope.hideLoader = hideLoader;
    $scope.showLoader();

    itemsService.getArchiveItems(function(data, status) {

        if (status < 200 || status >= 300)
            return;

        $scope.items = data;
        $scope.hideLoader();
    });
});

app.controller('SimpleController', function ($scope, itemsService) {});
;
