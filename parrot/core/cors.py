# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2020 by Farhan Ahmed.
    :license: See LICENSE for more details.
"""

"""
Module to enable Cross Origin Resource Sharing in Flask
Adapted from: https://github.com/crgwbr/flask_cors

Usage:
    from flask import Flask
    import re
    from errands.cors import CrossOriginResourceSharing

    app = Flask()

    # Allowed Origins
    allowed = (
        'http://localhost:9294', # Exact String Compare
        re.compile("^http([s]*):\/\/example.com([\:\d]*)$"), # Match a regex
    )

    # Add Access Control Header
    cors = CrossOriginResourceSharing(app)
    cors.set_allowed_origins(*allowed)

    Result:
    Access-Control-Allow-Headers: origin, x-requested-with, content-type, accept
    Access-Control-Allow-Origin: http://localhost:9294
    Access-Control-Allow-Credentials: True
    Access-Control-Allow-Methods: GET,POST,PUT,DELETE,OPTIONS
    Access-Control-Max-Age: 1728000

"""

import re
from flask import request


class CrossOriginResourceSharing:
    app = None
    allow_credentials = True
    allowed_origins = []
    max_age = 1728000
    methods = "GET,POST,PUT,DELETE,OPTIONS"

    def __init__(self, app):
        self.app = app
        self.app.after_request(self.process_request)

    def add_allowed_origin(self, origin):
        self.allowed_origins.append(origin)

    def add_allowed_origin_pattern(self, pattern):
        if isinstance(pattern, str):
            pattern = re.compile(pattern)
        self.allowed_origins.append(pattern)

    def allow_origin(self, response, origin):
        headers = request.headers.get("Access-Control-Request-Headers", "")

        response.headers["Access-Control-Allow-Headers"] = headers
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = self.allow_credentials
        response.headers["Access-Control-Allow-Methods"] = self.methods
        response.headers["Access-Control-Max-Age"] = self.max_age

        return response

    @classmethod
    def check_origin(cls, pattern):
        origin = request.headers.get("Origin", "")
        allowed = False
        if isinstance(pattern, str):
            if origin == pattern:
                allowed = True

        elif re.match(pattern, origin):
            allowed = True

        return allowed, origin

    def process_request(self, response):
        for pattern in self.allowed_origins:
            allowed, origin = self.check_origin(pattern)
            if allowed:
                self.allow_origin(response, origin)
                break

        return response

    def set_allow_credentials(self, allowed):
        self.allow_credentials = allowed

    def set_allowed_methods(self, *args):
        self.methods = ",".join(args)

    def set_allowed_origins(self, origin):
        self.allowed_origins = origin

    def set_max_age(self, max_age):
        self.max_age = max_age
