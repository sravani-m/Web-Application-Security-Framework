   �         Hhttps://geekflare.com/wp-content/themes/genesis/lib/js/skip-links.min.js     %�,3s�      %��]KX         
     H T T P / 1 . 1   2 0 0           �      Date   Sun, 28 Apr 2019 14:04:41 GMT   Content-Type   %application/javascript; charset=utf-8   Last-Modified   Wed, 30 Jan 2019 20:20:23 GMT   Etag   W/"5c520707-158"   Expires   Wed, 25 Apr 2029 14:04:41 GMT   Cache-Control   public, max-age=315360000   Access-Control-Allow-Origin   *   Cf-Cache-Status   HIT   Strict-Transport-Security   max-age=15552000; preload   X-Content-Type-Options   nosniff   	Expect-Ct   Wmax-age=604800, report-uri="https://report-uri.cloudflare.com/cdn-cgi/beacon/expect-ct"   Server   
cloudflare   Cf-Ray   4ce996384e49c93a-HYD   Content-Length   540                 // Injected by Arachni::Browser::Javascript
                _arachni_js_namespaceTaintTracer.update_tracers();
                _arachni_js_namespaceDOMMonitor.update_trackers();
function ga_skiplinks(){"use strict";var element=document.getElementById(location.hash.substring(1));element&&(!1===/^(?:a|select|input|button|textarea)$/i.test(element.tagName)&&(element.tabIndex=-1),element.focus())}window.addEventListener?window.addEventListener("hashchange",ga_skiplinks,!1):window.attachEvent("onhashchange",ga_skiplinks);;
