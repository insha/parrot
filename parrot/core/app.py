# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

import datetime
import logging
import logging.config
import os
import sys
import yaml
import re

from copy  import deepcopy
from flask import Flask, g, session, current_app

from .cors                  import CrossOriginResourceSharing
from .exceptions            import ParrotError, on_parrot_error, on_404, on_500
from .response              import APIEnpointResponse
from .service               import services, load_service_config
from .mail                  import mail
from parrot.blueprints.api  import constants as API

def create_app(config_file=None):
    """Factory to create the Flask application

    :param config_file: A python file from which to load the config.
                        If omitted, the config file must be set using
                        the ``PARROT_CONFIG`` environment variable.
                        If set, the environment variable is ignored
    :return: A `Flask` application instance
    """
    app = Flask('parrot')
    
    _setup_logger(app)
    _load_config(app, config_file)
    _setup_keys(app)
    _setup_extensions(app)
    _register_handlers(app)
    _register_blueprints(app)
    
    return app

def _setup_logger(app):
    # Create our customized logger.
    app._logger = logging.getLogger(app.logger.name)
    
    try:
        path = os.environ['PARROT_LOGGING_CONFIG']
    except KeyError:
        path = os.path.join(app.root_path, 'logging.yaml')
    
    with open(path) as f:
        logging.config.dictConfig(yaml.load(f))

def _load_config(app, config_file):
    app.config.from_pyfile('settings.py')
    
    if config_file:
        app.config.from_pyfile(config_file)
    else:
        app.config.from_envvar('PARROT_CONFIG', silent=True)
    
    if not app.config['ASSETS_FOLDER']:
        app.config['ASSETS_FOLDER'] = os.path.join(app.root_path, 'static', 'assets')
    
    if app.config['USE_PROXY']:
        app.wsgi_app = ProxyFix(app.wsgi_app)

def _setup_keys(app):
    """Configure the SECRET_KEY from a file in the instance directory.
    If the file does not exist, print instructions to create it from a 
    shell with a random key, then exit.
    """
    if app.config['PRODUCTION']:
        filename = os.path.join(app.instance_path, 'secret_key')
    
        try:
            app.config['SECRET_KEY'] = open(filename, 'rb').read()
        except IOError:
            print('Error: No secret key. Create it with:')
        
            full_path = os.path.dirname(filename)
        
            if not os.path.isdir(full_path):
                print('mkdir -p {path}'.format(path=full_path))
        
            print('head -c 24 /dev/urandom > {filename}'.format(filename=filename))
        
            sys.exit(1)
    else:
        # No keys need to be generated during development.
        pass

def _setup_extensions(app):
    mail.init_app(app)

def _register_handlers(app):
    # Custom Response for the API
    app.response_class = APIEnpointResponse
    
    # Register custom error handlers
    app.errorhandler(ParrotError)(on_parrot_error)
    app.errorhandler(404)(on_404)
    app.errorhandler(500)(on_500)
    
    if app.config.get('CORS_ENABLED', False):
        # Add Access Control Header
        cors    = CrossOriginResourceSharing(app)
        allowed = app.config.get('CORS_ALLOWED_ORIGINS', None)
        
        cors.set_allowed_origins(*allowed)
    else:
        # Nothing else needs to be done.
        pass
    
    # Register functions for handling before_request and teardown_request
    @app.before_request
    def before_request():
        g.service  = None
        g.app_info = current_app.config['APP_INFO']
        
        if API.SESSION_USER_AUTHENTICATION_TOKEN_KEY in session:
            g.service = services.find(identifier=session[API.SESSION_USER_AUTHENTICATION_TOKEN_KEY])

    @app.teardown_request
    def teardown_request(exception):
        g.service  = None
        g.app_info = None

def _register_blueprints(app):
    from parrot.blueprints.api import bp_api
    from parrot.blueprints.api import bp_api_config
    from parrot.blueprints.web import bp_web
    
    app.register_blueprint(bp_api_config)
    app.register_blueprint(bp_api)
    app.register_blueprint(bp_web)
