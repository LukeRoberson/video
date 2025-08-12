# Docker

This app can be run as a stand alone container, or part of a larger system using Docker Compose.
</br></br>


## Stand Alone Container

This is most useful if you want to run this service locally in your own home environment. It's a simple case of deploying a single container in Docker Server or in Docker Desktop.

See the **readme.md** file for details on how to get this up and running.
</br></br>


### Stable vs Development

There are two container tags in use:
* latest
* devel

As their names suggest, one is meant for 'production' and contains the latest stable updates.

The other is meant for development only, and is not considered stable.

Use the container with the _latest_ tag.
</br></br>


## Docker Compose

This is a more complex solution that you can use if you want to make the service accessible from outside your home network. This is an advanced option which will require you to have signigicant IT knowledge.
</br></br>

The components used in this solution are:
* Docker engine (docker server or docker desktop)
* This app as a container
* An NGINX container (to add certificates and other security)
* A domain name and DNS
* Port forwarding on your router
</br></br>

This page will focus on the container setup, and leave the domain, DNS, and port forwarding to you.
</br></br>

Sample compose file:

```yaml
services:
  frontend:
    image: "lukerobertson19/1320:latest"
    volumes:
      - c:\apps\local.db:/app/local.db
    restart: unless-stopped

  devel:
    image: "lukerobertson19/1320:devel"
    volumes:
      - c:\apps\local-devel.db:/app/local.db
    restart: unless-stopped

  proxy:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - c:\apps\nginx.conf:/etc/nginx/nginx.conf
      - c:\apps\nginx.key:/etc/ssl/certs/nginx.key
      - c:\apps\nginx.crt:/etc/ssl/certs/nginx.crt
      - c:\apps\dh-4096.pem:/etc/ssl/certs/dh-4096.pem
      - c:\apps\logs:/var/log/nginx
    restart: unless-stopped
```

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

First, create the **nginx.conf** in your local storage. It should look like this:

```
events {}
http {
    server {
        listen 80;
        server_name server.example.com;

        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl;
        server_name server.example.com;

        ssl_certificate /etc/ssl/certs/cert.pem;
        ssl_certificate_key /etc/ssl/certs/cert.pem;
        ssl_dhparam /etc/ssl/certs/dh-4096.pem;

        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_prefer_server_ciphers on;
        ssl_ciphers EECDH+AESGCM:EDH+AESGCM;
        ssl_ecdh_curve secp384r1;
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;
        ssl_session_tickets off;

        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";

        location / {
            proxy_pass http://frontend:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;        }
    }
}
```
</br></br>

This does several things:
* Sets up a service for server.example.com (change to suit your domain)
* Sets up a redirect from HTTP to HTTPS
* Uses the certificates that were generated earlier
* Sets up a proxy for the _frontend_ container (more on that next)
</br></br>


----
# Container Deployment

Now, we deploy the service using **Docker Compose**. It might be simpler to deploy _Portainer_ to manage this, but that's up to you.

The compose file looks like this:

```yaml
services:
  frontend:
    image: "lukerobertson19/1320:latest"
    volumes:
      - c:\apps\local.db:/app/local.db
    restart: unless-stopped

  proxy:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - c:\apps\nginx.conf:/etc/nginx/nginx.conf
      - c:\apps\nginx.key:/etc/ssl/certs/nginx.key
      - c:\apps\nginx.crt:/etc/ssl/certs/nginx.crt
      - c:\apps\dh-4096.pem:/etc/ssl/certs/dh-4096.pem
      - c:\apps\logs:/var/log/nginx
```

This deploys two containers. One is called _frontend_, which is the main web app container. There is no direct access to this container.

The other is called _proxy_, which is the NGINX container. This listens on ports 80 and 443.

When the NGINX container starts, it will receive web requests, and forward them to the frontend service.
