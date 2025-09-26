# Overview

NGINX is used as a front end to the solution to provide security. This is deployed as a container, and passes HTTP traffic to the application.

A configuration file (nginx.conf) is passed to NGINX at runtime.
</br></br>


## nginx.conf

```
events {}

http {
    # Enable HTTP/2 globally
    http2 on;

	# Bot detection
	map $http_user_agent $is_bot {
		default 0;
		~*bot 1;
		~*crawl 1;
		~*spider 1;
		~*scrape 1;
		"" 1;  # Empty user agent
	}

	# Common SSL settings
	ssl_protocols TLSv1.2 TLSv1.3;
	ssl_prefer_server_ciphers on;
	ssl_ciphers EECDH+AESGCM:EDH+AESGCM;
	ssl_ecdh_curve secp384r1;
	ssl_session_timeout 10m;
	ssl_session_cache shared:SSL:10m;
	ssl_session_tickets off;

	# Common security headers
	add_header X-Frame-Options DENY always;
	add_header X-Content-Type-Options nosniff always;
	add_header X-XSS-Protection "1; mode=block" always;
	add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

	# Common proxy headers
	proxy_set_header Host $host;
	proxy_set_header X-Real-IP $remote_addr;
	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	proxy_set_header X-Forwarded-Proto $scheme;
	proxy_set_header X-Forwarded-Host $host;

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name stream.networkdirection.net devel.networkdirection.net;
        return 301 https://$host$request_uri;
    }
	
    # Prod Container
    server {
        # Block obvious bots first
        if ($is_bot) {
            return 429;
        }
        
        # Strict limiting for suspicious patterns
        location ~* \.(php|asp|aspx|jsp)$ {
            return 444;
        }
        
        # Block common bot paths
        location ~* /(wp-admin|wp-login|phpmyadmin) {
            return 444;
        }

        listen 443 ssl;
        server_name stream.networkdirection.net;
        
        ssl_certificate /etc/ssl/certs/nginx.crt;
        ssl_certificate_key /etc/ssl/certs/nginx.key;
        ssl_dhparam /etc/ssl/certs/dh-4096.pem;

        location / {
            proxy_pass http://frontend:5000;
        }
    }

    # Dev Container
    server {
        # Block obvious bots first
        if ($is_bot) {
            return 429;
        }
        
        # Strict limiting for suspicious patterns
        location ~* \.(php|asp|aspx|jsp)$ {
            return 444;
        }
        
        # Block common bot paths
        location ~* /(wp-admin|wp-login|phpmyadmin) {
            return 444;
        }

        listen 443 ssl;
        server_name devel.networkdirection.net;
        
        ssl_certificate /etc/ssl/certs/nginx.crt;
        ssl_certificate_key /etc/ssl/certs/nginx.key;
        ssl_dhparam /etc/ssl/certs/dh-4096.pem;

        location / {
            proxy_pass http://devel:5000;
        }
    }
}

```
