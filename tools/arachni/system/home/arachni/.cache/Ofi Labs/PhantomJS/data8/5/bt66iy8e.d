   �         @http://testhtml5.vulnweb.com/static/app/services/itemsService.js     %� ��      %{g���              �      
     H T T P / 1 . 1   2 0 0      Content-Type   'application/x-javascript; charset=utf-8   Content-Length   919   Server   nginx/1.4.1   Date   Sat, 24 Jan 1970 03:09:39 GMT   Last-Modified   Fri, 10 May 2013 09:00:28 GMT   Etag   "518cb72c-2d3"   Expires   Mon, 23 Feb 1970 03:09:39 GMT   Cache-Control   max-age=2592000                 // Injected by Arachni::Browser::Javascript
                _arachni_js_namespaceTaintTracer.update_tracers();
                _arachni_js_namespaceDOMMonitor.update_trackers();
﻿app.service('itemsService', function ($http) {
    var items_per_page = 5;

    var items = [];

    this.getPopularItems = function (page, callback) {
        var offset = page * items_per_page;

        $http.get('/ajax/popular?offset=' + offset).success(callback);
    };

    this.getLatestItems = function (page, callback) {
        var offset = page * items_per_page;

        $http.get('/ajax/latest?offset=' + offset).success(callback);
    };

    this.getArchiveItems = function (callback) {
        $http.get('/ajax/archive').success(callback);
    };

    this.like = function (id, callback) {
        $http.get('/ajax/like?id=' + id).success(callback).error(callback);
    };

});
;
