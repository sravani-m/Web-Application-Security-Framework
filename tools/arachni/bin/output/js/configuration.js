jQuery(function ($) {
    var download_button = $('#configuration-download');

    // Create a blob object.
    var bb = new Blob(
        ["---\nscope:\n  redundant_path_patterns: {}\n  dom_depth_limit: 5\n  exclude_file_extensions: []\n  exclude_path_patterns: []\n  exclude_content_patterns: []\n  include_path_patterns: []\n  restrict_paths: []\n  extend_paths: []\n  url_rewrites: {}\nhttp:\n  user_agent: Arachni/v1.5.1\n  request_timeout: 10000\n  request_redirect_limit: 5\n  request_concurrency: 20\n  request_queue_size: 100\n  request_headers: {}\n  response_max_size: 500000\n  cookies: {}\n  authentication_type: auto\ninput:\n  values: {}\n  default_values:\n    name: arachni_name\n    user: arachni_user\n    usr: arachni_user\n    pass: 5543!%arachni_secret\n    txt: arachni_text\n    num: '132'\n    amount: '100'\n    mail: arachni@email.gr\n    account: '12'\n    id: '1'\n  without_defaults: false\n  force: false\nbrowser_cluster:\n  local_storage: {}\n  wait_for_elements: {}\n  pool_size: 6\n  job_timeout: 10\n  worker_time_to_live: 100\n  ignore_images: false\n  screen_width: 1600\n  screen_height: 1200\nsession: {}\naudit:\n  parameter_values: true\n  exclude_vector_patterns: []\n  include_vector_patterns: []\n  link_templates: []\n  links: true\n  forms: true\n  cookies: true\n  ui_inputs: true\n  ui_forms: true\n  jsons: true\n  xmls: true\ndatastore:\n  report_path: \nchecks:\n- xss_event\n- csrf\n- rfi\n- xss_path\n- source_code_disclosure\n- file_inclusion\n- no_sql_injection_differential\n- xss_dom_script_context\n- ldap_injection\n- os_cmd_injection_timing\n- code_injection_php_input_wrapper\n- trainer\n- sql_injection\n- xpath_injection\n- code_injection_timing\n- xss\n- unvalidated_redirect_dom\n- xxe\n- xss_script_context\n- path_traversal\n- sql_injection_differential\n- response_splitting\n- xss_tag\n- session_fixation\n- code_injection\n- xss_dom\n- unvalidated_redirect\n- sql_injection_timing\n- os_cmd_injection\n- no_sql_injection\n- insecure_cross_domain_policy_headers\n- interesting_responses\n- insecure_client_access_policy\n- localstart_asp\n- html_objects\n- password_autocomplete\n- insecure_cors_policy\n- unencrypted_password_forms\n- private_ip\n- hsts\n- x_frame_options\n- ssn\n- http_only_cookies\n- form_upload\n- insecure_cookies\n- credit_card\n- cookie_set_for_parent_domain\n- emails\n- cvs_svn_users\n- captcha\n- mixed_resource\n- origin_spoof_access_restriction_bypass\n- backup_files\n- insecure_cross_domain_policy_access\n- backup_directories\n- common_directories\n- allowed_methods\n- webdav\n- xst\n- htaccess_limit\n- http_put\n- backdoors\n- common_files\n- directory_listing\n- common_admin_interfaces\nplatforms: []\nplugins: {}\nno_fingerprinting: false\nauthorized_by: \nurl: http://testhtml5.vulnweb.com/\n"],
        { type : 'application/yaml' }
    );

    download_button.attr( 'href', window.URL.createObjectURL( bb ) );
    download_button.attr( 'download', 'testhtml5.vulnweb.com-profile.afp' );
});
