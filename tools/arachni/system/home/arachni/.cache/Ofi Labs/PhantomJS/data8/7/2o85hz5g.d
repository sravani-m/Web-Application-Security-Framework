   �         .http://testhtml5.vulnweb.com/static/app/app.js     %� ��      %{k���              �      
     H T T P / 1 . 1   2 0 0      Content-Type   'application/x-javascript; charset=utf-8   Content-Length   2080   Server   nginx/1.4.1   Date   Sat, 24 Jan 1970 03:09:38 GMT   Last-Modified   Tue, 14 May 2013 09:19:07 GMT   Etag   "5192018b-75c"   Expires   Mon, 23 Feb 1970 03:09:38 GMT   Cache-Control   max-age=2592000                 // Injected by Arachni::Browser::Javascript
                _arachni_js_namespaceTaintTracer.update_tracers();
                _arachni_js_namespaceDOMMonitor.update_trackers();
﻿function getPartialUrl(name) {
    return "/static/app/partials/" + name + ".html";
}

// app initialization
var app = angular.module('itemsApp', []);

//This configures the routes and associates each route with a view and a controller
app.config(function ($routeProvider) {
    $routeProvider
        .when('/popular',
        {
            controller: 'PopularItemsController',
            templateUrl: getPartialUrl('popular')
        })
        .when('/popular/page/:page',
        {
            controller: 'PopularItemsController',
            templateUrl: getPartialUrl('popular')
        })
        .when('/redir',
        {
            controller: 'SimpleController',
            templateUrl: getPartialUrl('redir')
        })
        .when('/all/filter/:filter',
        {
            controller: 'PopularItemsController',
            templateUrl: getPartialUrl('popular')
        })
        .when('/latest',
        {
            controller: 'LatestItemsController',
            templateUrl: getPartialUrl('latest')
        })
        .when('/latest/page/:page',
        {
            controller: 'LatestItemsController',
            templateUrl: getPartialUrl('latest')
        })
        .when('/carousel',
        {
            controller: 'PopularItemsController',
            templateUrl: getPartialUrl('carousel')
        })
        .when('/archive',
        {
            controller: 'ArchiveItemsController',
            templateUrl: getPartialUrl('archive')
        })
        .when('/about',
        {
            controller: 'SimpleController',
            templateUrl: getPartialUrl('about')
        })
        .when('/contact',
        {
            controller: 'SimpleController',
            templateUrl: getPartialUrl('contact')
        })
        .otherwise({ redirectTo: '/popular' });
});
;
