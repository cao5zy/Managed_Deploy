{% for item in items %}
upstream	{{item.project_name}} {
		server	     {{'{{'}}{{item.project_name}}{{'}}'}}:{{'{{'}}{{item.project_name}}_port{{'}}'}};
		keepalive    2000;
}
{% endfor %}

server {
       listen				{{'{{'}}public_port{{'}}'}};
       server_name				{{'{{'}}microservice_gate{{'}}'}};
       access_log				logs/access.log;

{% for item in items %}
      location /_api/{{item.project_name}}/ {
	resolver	{{'{{'}}auth_db_ip{{'}}'}} valid=30s;
	set 	$auth_db {{'{{'}}auth_db_ip{{'}}'}};
	set 	$auth_db_port {{'{{'}}auth_db_port{{'}}'}};
	rewrite_by_lua_file		/lua_app/access.lua;
      
	proxy_pass http://{{item.project_name}}/;
	proxy_set_header Host $host:$server_port;
	log_subrequest on;
	log_not_found on;
	error_log logs/{{item.project_name}}.error.log debug;
	access_log logs/{{item.project_name}}.access.log;
	allow	   all;
      }

{% endfor %}

       location /signup {
             resolver	{{'{{'}}auth_db_ip{{'}}'}} valid=30s;
             set 	$auth_db {{'{{'}}auth_db_ip{{'}}'}};
       	     set 	$auth_db_port {{'{{'}}auth_db_port{{'}}'}};
       	     rewrite_by_lua_file		/lua_app/signup.lua;

             error_log logs/signup.error.log debug;
	     access_log logs/signup.access.log;
	     allow	   all;
       }
       location /signin {
             resolver	{{'{{'}}auth_db_ip{{'}}'}} valid=30s;
             set 	$auth_db {{'{{'}}auth_db_ip{{'}}'}};
       	     set 	$auth_db_port {{'{{'}}auth_db_port{{'}}'}};
       	     rewrite_by_lua_file		/lua_app/signin.lua;

             error_log logs/signin.error.log debug;
       	     access_log logs/signin.access.log;
       	     allow	   all;
       }
       location /test_html {
             include       mime.types;
             default_type  application/octet-stream;
	     sendfile        on;
	     keepalive_timeout  65;

             gzip on;
             gzip_types text/plain application/x-javascript text/css application/xml text/javascript application/javascript image/jpeg image/gif image/png;
	     gzip_vary on;

             root /lua_app;
             index index.html;

             resolver	{{'{{'}}auth_db_ip{{'}}'}} valid=30s;
             set 	$auth_db {{'{{'}}auth_db_ip{{'}}'}};
       	     set 	$auth_db_port {{'{{'}}auth_db_port{{'}}'}};

       	     rewrite_by_lua_file		/lua_app/access.lua;

             error_log logs/test_html.error.log debug;
       	     access_log logs/test_html.access.log;
       	     allow	   all;

       }

}