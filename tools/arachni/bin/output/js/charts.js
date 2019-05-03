function index_to_shortname( index ){
    return ["xss_script_context","xss","xss_dom","csrf","unvalidated_redirect_dom","xss_dom_script_context","common_directories","unencrypted_password_forms","x_frame_options","insecure_cors_policy","password_autocomplete","http_only_cookies","interesting_responses","allowed_methods"][index];
}

function index_to_severity( index ){
    return {"xss_script_context":"high","xss":"high","xss_dom":"high","csrf":"high","unvalidated_redirect_dom":"high","xss_dom_script_context":"high","common_directories":"medium","unencrypted_password_forms":"medium","x_frame_options":"low","insecure_cors_policy":"low","password_autocomplete":"low","http_only_cookies":"informational","interesting_responses":"informational","allowed_methods":"informational"}[index_to_shortname(index)];
}

function renderCharts() {
    if( window.renderedCharts )
    window.renderedCharts = true;

    c3.generate({
        bindto: '#chart-issues',
        data: {
            columns: [
                ["Trusted",1,5,1,1,1,1,1,1,1,1,1,1,5,1],
                ["Untrusted",0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                ["Severity",4,4,4,4,4,4,3,3,2,2,2,1,1,1]
            ],
            axes: {
                Severity: 'y2'
            },
            type: 'bar',
            groups: [
                ['Trusted', 'Untrusted']
            ],
            types: {
                Severity: 'line'
            },
            onclick: function (d) {
                var location;

                if( d.name.toLowerCase() == 'severity' ) {
                    location = 'summary/issues/trusted/severity/' + index_to_severity(d.x);
                } else {
                    location = 'summary/issues/' + d.name.toLowerCase() + '/severity/' +
                        index_to_severity(d.x) + '/' + index_to_shortname(d.x);
                }

                goToLocation( location );
            }
        },
        regions: [{"class":"severity-high","start":0,"end":5},{"class":"severity-medium","start":6,"end":7},{"class":"severity-low","start":8,"end":10},{"class":"severity-informational","start":11}],
        axis: {
            x: {
                type: 'category',
                categories: ["Cross-Site Scripting (XSS) in script context","Cross-Site Scripting (XSS)","DOM-based Cross-Site Scripting (XSS)","Cross-Site Request Forgery","Unvalidated DOM redirect","DOM-based Cross-Site Scripting (XSS) in script context","Common directory","Unencrypted password form","Missing 'X-Frame-Options' header","Insecure 'Access-Control-Allow-Origin' header","Password field with auto-complete","HttpOnly cookie","Interesting response","Allowed HTTP methods"],
                tick: {
                    rotate: 15
                }
            },
            y: {
                label: {
                    text: 'Amount of logged issues',
                    position: 'outer-center'
                }
            },
            y2: {
                label: {
                    text: 'Severity',
                    position: 'outer-center'
                },
                show: true,
                type: 'category',
                categories: [1, 2, 3, 4],
                tick: {
                    format: function (d) {
                        return ["Informational","Low","Medium","High"][d - 1]
                    }
                }
            }
        },
        padding: {
            bottom: 40
        },
        color: {
            pattern: [ '#1f77b4', '#d62728', '#ff7f0e' ]
        }
    });

    c3.generate({
        bindto: '#chart-trust',
        data: {
            type: 'pie',
            columns: [["Trusted",22],["Untrusted",0]]
        },
        pie: {
            onclick: function (d) { goToLocation( 'summary/issues/' + d.id.toLowerCase() ) }
        },
        color: {
            pattern: [ '#1f77b4', '#d62728' ]
        }
    });

    c3.generate({
        bindto: '#chart-elements',
        data: {
            type: 'pie',
            columns: [["form",3],["link",3],["link_dom",2],["cookie",4],["cookie_dom",1],["server",9]]
        }
    });

    c3.generate({
        bindto: '#chart-severities',
        data: {
            type: 'pie',
            columns: [["high",10],["medium",2],["low",3],["informational",7]]
        },
        color: {
            pattern: [ '#d62728', '#ff7f0e', '#ffbb78', '#1f77b4' ]
        },
        pie: {
            onclick: function (d) {
                goToLocation( 'summary/issues/trusted/severity/' + d.id );
            }
        }
    });

}
