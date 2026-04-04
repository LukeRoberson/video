"""
Module: dev_proxy.py

Sets up a proxy route for development purposes, allowing the browser
    to communicate with the API.
This is needed because TypeScript files use relative paths to access
    the API. In production, NGINX will handle this routing, but in
    development, we need to set up a proxy route in the Flask application

Routes:
    /api/* -> Proxies to the backend API server

Dependencies:
    Flask
    Requests
"""

from flask import (
    Blueprint,
    Response,
    request,
    current_app
)
import requests


dev_proxy_bp = Blueprint(
    'dev_proxy',
    __name__
)


@dev_proxy_bp.route(
    '/api/',
    defaults={'path': ''},
    methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
)
@dev_proxy_bp.route(
    '/api/<path:path>',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
)
def proxy_api(path):
    base_url = current_app.config.get(
        'API_BASE_URL',
        'http://localhost:5010'
    )
    url = f"{base_url}/api/{path}"

    # Forward headers, dropping hop-by-hop headers
    headers = {
        k: v for k, v in request.headers
        if k.lower() not in ('host', 'content-length')
    }

    response = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        params=list(request.args.items(multi=True)),
        allow_redirects=False,
        timeout=30,
    )

    # Drop hop-by-hop response headers that would confuse Flask
    excluded = {'content-encoding', 'transfer-encoding', 'connection'}
    response_headers = {
        k: v for k, v in response.headers.items()
        if k.lower() not in excluded
    }

    return Response(
        response.content,
        status=response.status_code,
        headers=response_headers
    )
