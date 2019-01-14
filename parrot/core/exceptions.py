# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

from flask import jsonify

from parrot.blueprints.api import constants as API

##############
# Exceptions #
##############
class ParrotError(Exception):
    """Base API application error class."""
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        
        if status_code is not None:
            self.status_code = status_code
        
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


##################
# Error Handlers #
##################

def on_parrot_error(error):
    response             = jsonify(error.to_dict())
    response.status_code = error.status_code
    
    return response

def on_404(e):
    return jsonify(dict(error='Not found')), API.HTTP_STATUS_CODE_NOT_FOUND

def on_500(e):
    return jsonify(dict(error='Server error')), API.HTTP_STATUS_CODE_INTERNAL_SERVER_ERROR
