# Overview

NGINX is used as a front end to the solution to provide security. This is deployed as a container, and passes HTTP traffic to the application.

A configuration file (nginx.conf) is passed to NGINX at runtime.
</br></br>


## nginx.conf

```
events {}

http {
	# Rate Limiting
	limit_req_zone $binary_remote_addr zone=general:10m rate=240r/m;
	limit_req_zone $binary_remote_addr zone=strict:10m rate=40r/m;
	limit_req_zone $binary_remote_addr zone=api:10m rate=240r/m;
	limit_req_zone $binary_remote_addr zone=not_found:10m rate=60r/m;

	# Bot detection
	map $http_user_agent $is_bot {
		default 0;
		~*bot 1;
		~*crawl 1;
		~*spider 1;
		~*scrape 1;
		"" 1;  # Empty user agent
	}

    # Redirect HTTP to HTTPS
	server {
		listen 80;
		server_name stream.networkdirection.net;
		
		location / {
			return 301 https://$host$request_uri;
		}
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
		
		ssl_protocols TLSv1.2 TLSv1.3;
		ssl_prefer_server_ciphers on;
		ssl_ciphers EECDH+AESGCM:EDH+AESGCM;
		ssl_ecdh_curve secp384r1;
		ssl_session_timeout 10m;
		ssl_session_cache shared:SSL:10m;
		ssl_session_tickets off;
		
		add_header X-Frame-Options DENY;
		add_header X-Content-Type-Options nosniff;
		add_header X-XSS-Protection "1; mode=block";
			
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Static assets (adjust extensions as needed)
        location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
            proxy_pass http://frontend:5000;
            expires 1d;
            add_header Cache-Control "public, immutable";
        }

        # Whitelist Known Routes
		location = / {
			proxy_pass http://frontend:5000;
            limit_req zone=general burst=10 nodelay;

			proxy_set_header Host $host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header X-Forwarded-Proto $scheme;
		}

        # Handle 404s with strict rate limiting
        error_page 404 = @not_found;
        location @not_found {
            limit_req zone=not_found burst=3 nodelay;
            return 404;
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
		
		ssl_protocols TLSv1.2 TLSv1.3;
		ssl_prefer_server_ciphers on;
		ssl_ciphers EECDH+AESGCM:EDH+AESGCM;
		ssl_ecdh_curve secp384r1;
		ssl_session_timeout 10m;
		ssl_session_cache shared:SSL:10m;
		ssl_session_tickets off;
		
		add_header X-Frame-Options DENY;
		add_header X-Content-Type-Options nosniff;
		add_header X-XSS-Protection "1; mode=block";
			
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Static assets (adjust extensions as needed)
        location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
            proxy_pass http://devel:5000;
            expires 1d;
            add_header Cache-Control "public, immutable";
        }

		location / {
			proxy_pass http://devel:5000;
            limit_req zone=general burst=10 nodelay;
			
			proxy_set_header Host $host;
			proxy_set_header X-Real-IP $remote_addr;
			proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
			proxy_set_header X-Forwarded-Proto $scheme;
		}

        # Handle 404s with strict rate limiting
        error_page 404 = @not_found;
        location @not_found {
            limit_req zone=not_found burst=3 nodelay;
            return 404;
        }
	}
}

```
