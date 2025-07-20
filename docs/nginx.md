# Overview

NGINX is used as a front end to the solution to provide security. This is deployed as a container, and passes HTTP traffic to the application.

A configuration file (nginx.conf) is passed to NGINX at runtime.
</br></br>


## nginx.conf

```
# Rate Limiting
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/m;
limit_req_zone $binary_remote_addr zone=strict:10m rate=2r/m;
limit_req_zone $binary_remote_addr zone=api:10m rate=30r/m;

# Track 404 errors
limit_req_zone $binary_remote_addr zone=not_found:10m rate=5r/m;

# Bot detection
map $http_user_agent $is_bot {
    default 0;
    ~*bot 1;
    ~*crawl 1;
    ~*spider 1;
    ~*scrape 1;
    "" 1;  # Empty user agent
}

events {}

http {
    # Redirect HTTP to HTTPS
	server {
		listen 80;
		server_name stream.networkdirection.net;
		
		location / {
			return 301 https://$host$request_uri;
		}
	}
	
    # HTTPS Configuration
	server {
        # Block obvious bots first
        if ($is_bot) {
            return 429;
        }
        
        # General rate limiting
        limit_req zone=general burst=20 nodelay;
        
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
		location / {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /about {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /characters {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /character {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /speakers {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /speaker {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /scriptures {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /scripture {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /tags {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /tag {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /broadcasting {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /children {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /teens {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /family {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /programs_events {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /our_activities {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /meetings_ministry {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /organization {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /bible {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /dramas {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /series {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /music {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /interviews {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /video {
            limit_req zone=general burst=10 nodelay;
			proxy_pass http://frontend:5000;
		}

		location /admin {
            limit_req zone=strict burst=5 nodelay;
			proxy_pass http://frontend:5000;
		}

        location ^~ /api/ {
            limit_req zone=api burst=10 nodelay;
            proxy_pass http://frontend:5000;
        }

        # Default deny for any unmatched routes
        location / {
            return 404;
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
