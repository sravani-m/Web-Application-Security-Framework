   �         /http://testhtml5.vulnweb.com/static/app/post.js     %� ��      %{n���              �      
     H T T P / 1 . 1   2 0 0      Content-Type   'application/x-javascript; charset=utf-8   Content-Length   3515   Server   nginx/1.4.1   Date   Sat, 24 Jan 1970 03:09:38 GMT   Last-Modified   Fri, 17 May 2013 12:18:21 GMT   Etag   "5196200d-cf7"   Expires   Mon, 23 Feb 1970 03:09:38 GMT   Cache-Control   max-age=2592000                 // Injected by Arachni::Browser::Javascript
                _arachni_js_namespaceTaintTracer.update_tracers();
                _arachni_js_namespaceDOMMonitor.update_trackers();
// post AngularJs init

// modal login form
$('#loginFormSubmit').on('click', function(e){
    // We don't want this to act as a link so cancel the link action
    e.preventDefault();
    // Find form and submit it
    $('#loginForm').submit();
});

$('#loginFormForgot').on('click', function(e){
    // We don't want this to act as a link so cancel the link action
    e.preventDefault();

    // submit password request
    $.ajax({
        url: "/forgotpw",
        data: "<forgot><username>" + $('#username').attr("value") + "</username></forgot>",
        type: 'POST',
        contentType: "text/xml",
        dataType: "text",
        success : function(data){
            alert(data + ", your password was changed. You will receive an email with the new password shortly.");
        },
        error : function (xhr, ajaxOptions, thrownError){
            console.log(xhr.status);
            console.log(thrownError);
        }
    });
});

// when a nav link is clicked make the link active
$('.nav li a').on('click', function(e){
    var url = $(this).attr("href");
    if (url.indexOf("http://") != 0 && url.indexOf("/admin/") != 0)
        e.preventDefault(); // prevent link click

    var $thisLi = $(this).parent('li');
    var $ul = $thisLi.parent('ul');

    if (!$thisLi.hasClass('active'))
    {
        $ul.find('li.active').removeClass('active');
        $thisLi.addClass('active');
    }
})

// loader
showLoader = function () {
    $("#loader").show();
}

hideLoader = function () {
    $("#loader").hide();
}

// take care of URL from hash
$('.nav li a').each(function(){
    var $thisLi = $(this).parent('li');
    if ($thisLi.hasClass('active'))
        $thisLi.removeClass('active');
})

var foundPath = false;
$('.nav li a').each(function(){
    var $thisLi = $(this).parent('li');
    if ($(this).attr("href") == location.hash)
    {
        $thisLi.addClass('active');
        foundPath = true;
    }
})

if (!foundPath) {
    $('#popularLi').addClass('active');
}

// cookies
function getCookie(c_name)
{
    var c_value = document.cookie;
    var c_start = c_value.indexOf(" " + c_name + "=");
    if (c_start == -1)
    {
        c_start = c_value.indexOf(c_name + "=");
    }
    if (c_start == -1)
    {
        c_value = null;
    }
    else
    {
        c_start = c_value.indexOf("=", c_start) + 1;
        var c_end = c_value.indexOf(";", c_start);
        if (c_end == -1)
        {
            c_end = c_value.length;
        }
        c_value = unescape(c_value.substring(c_start,c_end));
    }
    return c_value;
}

var cookieUsername = getCookie("username");
if (!cookieUsername) cookieUsername = "unknown";

// referrer and sessvars
var referrer = "unknown";
if (document.referrer) {referrer = document.referrer;}

sessvars.pageCount=sessvars.pageCount||0;
sessvars.pageCount++;

$("#refId").html(cookieUsername + " is coming from <b>" + referrer + "</b> and has visited this page <b>" + (sessvars.pageCount)  + "</b> times.");

// facebook
var hrf=window.location.href.toLowerCase();
if (hrf !='http://www.facebook.com/')
    document.write('<div class="fb-comments" data-num-posts="4" data-width="470"  data-href="'+window.location.href+'"></div>')

;
