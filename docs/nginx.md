# Overview

NGINX is used as a front end to the solution to provide security. This is deployed as a container, and passes HTTP traffic to the application.

A configuration file (nginx.conf) is passed to NGINX at runtime.
</br></br>


## Rate Limiting

limit_req_zone $binary_remote_addr zone=general:10m rate=10r/m;
limit_req_zone $binary_remote_addr zone=strict:10m rate=2r/m;
limit_req_zone $binary_remote_addr zone=api:10m rate=30r/m;
</br></br>


## Track 404 errors
limit_req_zone $binary_remote_addr zone=not_found:10m rate=5r/m;

server {
    # General rate limiting
    limit_req zone=general burst=20 nodelay;
    
    # Strict limiting for suspicious patterns
    location ~* \.(php|asp|aspx|jsp)$ {
        return 444;  # Close connection without response
    }
    
    # Block common bot paths
    location ~* /(wp-admin|wp-login|admin|phpmyadmin) {
        return 444;
    }
    
    # Your app routes (adjust based on your actual routes)
    location / {
        limit_req zone=api burst=10 nodelay;
        proxy_pass http://your-app;
    }
    
    # Handle 404s with strict rate limiting
    error_page 404 = @not_found;
    location @not_found {
        limit_req zone=not_found burst=3 nodelay;
        return 404;
    }
}
</br></br>


## Whitelist Known Routes

server {
    # Default deny
    location / {
        return 404;
    }
    
    # Explicitly allow your app routes
    location = / {
        proxy_pass http://your-app;
    }
    
    location /api/videos {
        proxy_pass http://your-app;
    }
    
    location /upload {
        proxy_pass http://your-app;
    }
    
    # Add other specific routes your app uses
    location /static/ {
        proxy_pass http://your-app;
    }
}
</br></br>


