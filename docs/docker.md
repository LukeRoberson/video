# Docker

This app is designed to be deployed using Docker Compose. This is beacuse there are several containers in use:
* Frontend (the UI)
* Backend (the API and database)
* ElasticSearch
* Nginx reverse proxy
</br></br>

> [!NOTE]
> This project is available as 'prod' and 'devel'.
> 'prod' is the stable release, and 'devel' is used for testing new features.



## Compose Environment

The included `docker-compose.yaml` file shows how this deploys these four containers, or services, to make a complete app.
</br></br>


### Containers

| Name          | Notes                                                  | Relies on         |
| ------------- | ------------------------------------------------------ | ----------------- |
| backend       | The API and database services                          | ElasticSearch*    |
| frontend      | The UI for the application                             | backend           |
| elasticsearch | 3rd party container; Enables deep searching of content |                   |
| proxy         | 3rd party container; The NGINX reverse proxy           | frontend, backend |
</br></br>


> [!NOTE]
> The backend can work without the ElasticSearch service.
> However, for full functionality, this should be running before the backend starts
</br></br>



### Network

There is a 'bridge' network named `private` for all containers to communicate with each other.

Only the proxy service has any network exposure to the outside network. All requests to the app come through this service. This is to enforce HTTP routing as well as security.
</br></br>


The proxy service listens on ports 80 and 443 for the production deployment.

It also listens on ports 8080 and 8443 for the devel deployment. This allows both to be be deployed on the same system without port conflicts.

Typically however, just the production environment will be used.
</br></br>



### Storage

There is one named volume, called `esdata`. This is for the ElasticSearch service.

There are also several bind mounts, which are used in the backend and proxy services.

The backend service uses a bind mount for the `local.db` database file. This means this file is stored directly on the host system, and can easily be backed up by the system administrator.

The proxy service has several bind mounts, which are used for configuration files, log files, and certificate files. More on how these are used in later sections.
</br></br>



### Environment Variables

Environment variables are used in several places for configuring the application.
</br></br>


#### Backend Service

The backend service uses the `ELASTICSEARCH_HOST` and `ELASTICSEARCH_PORT` variables to find the elastic search service. By default, the ElasticSearch container will listen on TCP port 9200.

These variables are configured directly in the compose file.
</br></br>


The backend service also uses the `LOCAL_DB_PATH` variable in a bind mount. This is the location of the `local.db` file on the local system.

This variable needs to be set when the app is started.
</br></br>


#### Frontend Service

The frontend service uses the `API_BASE_URL` variable, to define how to reach the backend service. This uses TCP port 5010 by default.

This variable is defined in the compose file.
</br></br>


#### Proxy Service

The proxy service uses five variables in its bind mount configuration. All of these are set at runtime, not in the compose file.

`NGINX_CONF_PATH` defines the location of the `nginx.conf` file on the local system.

`NGINX_CRT_PATH` defines the local location of the certificate PEM file.

`NGINX_KEY_PATH` defines the local location of the certificate KEY file.

`DH_PARAM_PATH` defines the local location of the DH key file.

`NGINX_LOG_PATH` defines the local location of the log files that NGINX generates.
</br></br>


Optional environment variables can be used to change which ports are used on the outside. For example, if the standard ports are already in use.

`HTTP_PORT` is the standard HTTP port. Defaults to 80.

`HTTPS_PORT` is the secure HTTP port. Defaults to 443.

> [!NOTE]
> Changing the porst here affects the container deployment.
> The NGINX config file will still need to be updated accordingly.
</br></br>


The NGINX configuration file is stored locally so an admin can change the configuration as needed for the local environment.

The log files are stored locally so an admin can easily troubleshoot, if needed.

The certificate files are stored locally so they can be replaced as needed.
</br></br>


### Build Files

The frontend and backend containers are custom, so they need to be built into containers using docker files. ElasticSearch and NGINX are both 3rd party services, so these containers can just be downloaded.
</br></br>


This project includes `Dockerfile.backend` and `Dockerfile.frontend` for the backend and frontend services.

While these can be built manually with docker commands, it's also easy to contain the build process in the compose file.

The included compose file includes the required configuration to do this automatically when the app starts.
</br></br>




----
# Domain Names and DNS

If you want this service to be available over the internet, you will need to have a registered domain, and DNS to manage records in the domain.

Alternatively, you could run this locally in your home environment with your own private domain and DNS.

The third option is not to use DNS at all, and just access the container by an IP address. However, this won't support TLS/certificates/HTTPS.
</br></br>




----
# Certificates

When running as a full service, NGINX will need certificates to run over HTTPS. These can be:
* Self-signed - Easier to set up, but less secure
* Issued by a CA - More secure, but requires a domain name and some setup
</br></br>


## Self Signed Certificates

To generate a self signed certificate, the easiest option is to use the **alpine/openssl** container. This is easier, as you already have a container environment, so you don't need to install anything. Of course, if you have access to openssl some other way, that will be fine too.

When using this container, we use docker run commands to start the container, and we pass openssl commands, all in one line.
</br></br>


## Docker Commands

The basic docker command is:

```bash
docker run --rm -it --name openssl --mount type=bind,src=/your/local/path,dst=openssl-data alpine/openssl <<openssl commands>>
```

| Component      | Description                                                         |
| -------------- | ------------------------------------------------------------------- |
| --rm           | Remove container when the job is done                               |
| -it            | Interactive session with pseudo-TTY (so we can access the terminal) |
| --name         | Optional. A custom name for the container                           |
| --mount        | Attach a filesystem. We need this to save files                     |
| type=bind      | Use a bind mount rather than a volume                               |
| src and dst    | src is your local path, dst is the path within the container        |
| alpine/openssl | The image name to build the container from                          |
</br></br>


## Openssl Commands

Normally, openssl commands work like this:

```bash
openssl <<options>>
```

In our case, we replace _openssl_ with the docker command previously shown.
</br></br>


### RSA Certificate

To generate the certificate, use this command (replace openssl with the docker command):

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /openssl-data/nginx.key -out /openssl-data/nginx.crt
```

This will start an interactive process to generate a certificate. When done, it will leave it in your local directory.
</br></br>


### DH Key

To generate a DH key (will take a while to run):

```bash
openssl dhparam -out /openssl-data/dh-4096.pem 4096
```
</br></br>


----
# NGINX Configuration

As noted before, the `nginx.conf` file, that is the file for NGINX configuration, is not included natively in this project, and needs to be stored on the local system.

First, create the `nginx.conf` in your local storage. It should look like this:

```nginx
events {}

http {
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
  add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'" always;

  # Common proxy headers
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto $scheme;
  proxy_set_header X-Forwarded-Host $host;

  # HTTP Routes: Redirect to HTTPS
  server {
    listen 80;
    server_name server.example.com;
    return 301 https://$host$request_uri;
  }

  # HTTPS routes
  server {
    # HTTPS specific settings
    listen 443 ssl;
    http2 on;
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

    server_name server.example.com;

    ssl_certificate /etc/ssl/certs/nginx.crt;
    ssl_certificate_key /etc/ssl/certs/nginx.key;
    ssl_dhparam /etc/ssl/certs/dh-4096.pem;

    # Frontend UI
    location / {
        proxy_pass http://frontend:5000;
    }

    # API route
    location /api {
        proxy_pass http://backend:5010;
    }
  }
}
```
</br></br>


This assumes deployment of the 'prod' service, which uses ports 80 (HTTP) and 443 (HTTPS).

You can modify this sample configuration to your needs, or use it just as it is.

> [!WARNING]
> This uses specific filenames for certificate files, such as 'nginx.cert'.
> If you use different file names, make sure you update this file accordingly.
</br></br>

> [!NOTE]
> This example uses 'server.example.com'.
> Update this as needed for your local environment.
</br></br>


This configuration does several things:
* Sets up a service for server.example.com (change to suit your domain)
* Sets up a redirect from HTTP to HTTPS
* Uses the certificates that were generated earlier
* Sets up a proxy for the _frontend_ container (the UI)
* Sets up a proxy for the _backend_ container (the API)
</br></br>

