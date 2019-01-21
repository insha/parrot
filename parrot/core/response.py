# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

import time

from werkzeug.datastructures import Headers
from flask import jsonify, Response, current_app

from parrot.blueprints.api import constants as API
from parrot.utils.codes import get_random_code


class ServiceResponse(object):
    def __init__(self, **kwargs):
        self.status_code = kwargs.get('status_code', API.HTTP_STATUS_CODE_OK)
        self.error_code = kwargs.get('error_code', API.RESPONSE_RESULT_SUCCESS)
        self.message = kwargs.get('message', None)
        self.content = kwargs.get('content', None)
        self.errors = kwargs.get('errors', None)
        self.lag = kwargs.get('lag', 0)
        self.fuzz = kwargs.get('fuzz', False)
        self.headers = kwargs.get('headers', {'content-type': 'application/json'})

    def __repr__(self):
        return '<%s %r (%r)>' % (self.__class__.__name__, self.content, self.error_code)

    def to_json(self):
        template = {}

        if self.content:
            template = self.content

        if self.error_code != API.RESPONSE_RESULT_SUCCESS:
            template[API.RESPONSE_ERROR_KEY] = {
                API.RESPONSE_ERROR_CODE_KEY: self.error_code,
                API.RESPONSE_MESSAGE_KEY: self.message,
            }

            if self.errors:
                template[API.RESPONSE_ERROR_KEY][
                    API.RESPONSE_ERROR_LIST_KEY
                ] = self.errors

        json_response = jsonify(template)
        json_response.status_code = self.status_code

        return json_response


class APIEnpointResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, ServiceResponse):
            rv = rv.to_json()
        else:
            # Nothing to do
            pass

        return super(APIEnpointResponse, cls).force_type(rv, environ)
