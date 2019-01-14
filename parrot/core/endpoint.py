# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

import uuid

from flask import current_app

from .response import ServiceResponse
from parrot.blueprints.api import constants as API

class ServiceEndpoint(object):
    url         = None
    parameters  = None
    responses   = {}
    identifier  = None
    description = ''
    
    def __init__(self, url=None, parameters=None, description='', responses=[]):
        identifier = str(uuid.uuid1())
        
        if url:
            self.url         = url
            self.parameters  = parameters
            self.responses   = {}
            self.description = description
            
            for response in responses:
                self.responses[response.method] = response
    
    def __repr__(self):
        return '<ServiceEndpoint {memory}> {endpoint}'.format(memory=hex(id(self)), endpoint=self.url)
    
    def find(self, method=None, url=None):
        service_response = None
        
        try:
            if self.url == url:
                service_response = self.responses[method.upper()]
        except:
            current_app.logger.info('Could not find the response for {method}/{url}'.format(method=method, url=url))
        
        return service_response

    def add_response(self, payload=None):
        method       = payload.get(API.RESPONSE_PAYLOAD_METHOD_KEY, API.DEFAULT_METHOD)
        status_code  = payload.get(API.RESPONSE_PAYLOAD_STATUS_CODE_KEY, API.DEFAULT_STATUS_CODE)
        headers      = payload.get(API.RESPONSE_PAYLOAD_HEADERS_KEY, API.DEFAULT_HEADER)
        content      = payload.get(API.RESPONSE_PAYLOAD_CONTENT_KEY)
        lag          = payload.get(API.RESPONSE_PAYLOAD_LAG_KEY, 0)
        fuzz         = payload.get(API.RESPONSE_PAYLOAD_FUZZ_KEY, False)
        
        service_response = ServiceResponse(status_code=status_code, 
                                           method=method, 
                                           headers=headers, 
                                           content=content)
        service_response.lag  = lag
        service_response.fuzz = fuzz
        
        self.responses[method.upper()] = service_response
