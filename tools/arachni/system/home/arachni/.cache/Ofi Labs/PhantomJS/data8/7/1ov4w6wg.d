   �         "http://bxss.s3.amazonaws.com/ad.js�       ����      %{n
P              �      
     H T T P / 1 . 1   2 0 0   	   
X-Amz-Id-2   L5jo6fOEjt27uYwf5zQam1Sx+TsPKsQEf1OUdN+PoPYZaNb+voCJKeABW0kwqGbS8XCrYIWBvHBg=   X-Amz-Request-Id   7C77DF321615C978   Date   Sun, 28 Apr 2019 12:49:35 GMT   Last-Modified   Fri, 17 May 2013 14:09:54 GMT   Etag   ""14d265272db98157955d1fc252e2c5a4"   X-Amz-Meta-Cb-Modifiedtime   Fri, 17 May 2013 13:52:57 GMT   Content-Type   'application/x-javascript; charset=utf-8   Content-Length   1189   Server   AmazonS3                 // Injected by Arachni::Browser::Javascript
                _arachni_js_namespaceTaintTracer.update_tracers();
                _arachni_js_namespaceDOMMonitor.update_trackers();
// this is a third part script from an ad provider
// this code is vulnerable to DOM XSS and is affecting all the sites that are including it

ads_ad_zone = "234";
ads_ad_client = "723898932";
ads_ad_width = "1";
ads_ad_height = "1";
ads_ad_pn = "";

(
function()
{
    var iframe_properties = {
        zone_id : ads_ad_zone,
        ad_client : ads_ad_client,
        u_h : screen.height,
        u_w : screen.width,
        pn : ads_ad_pn,
        ref : document.referrer,
        url : window.location
    };

    var iframe_url = 'http://ads.bxss.me/ad_server.php?';

    for (var x in iframe_properties)
    {
        iframe_url += x+'='+iframe_properties[x]+'&';
    }

    document.write('<iframe name="ads_ads_frame" src="'+iframe_url+'" marginwidth="0" marginheight="0" vspace="0" hspace="0" allowtransparency="true" frameborder="0" height="'+ads_ad_height+'" scrolling="no" width="'+ads_ad_width+'" style="background-color:#FFFFFF;"></iframe>');
}
)();
