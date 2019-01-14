# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

# This file defines default config values and is loaded right before
# the file specified in the PARROT_CONFIG environment variable is
# loaded.

import os

from parrot import __app_info__

PROJECT_PATH            = os.path.abspath(os.path.dirname(__file__))
BUNDLE_FOLDER           = 'bundles'
RESPONSES_FOLDER        = 'responses'
SITE_ROOT               = os.path.realpath(os.path.dirname(__file__))
CONFIG_PATH             = os.path.join(SITE_ROOT, BUNDLE_FOLDER)
CONFIGURATION_FILE_NAME = 'config.json'

APP_INFO = __app_info__
ADMINS   = ['your_name@example.com']

ASSETS_FOLDER           = None
USE_PROXY               = False
SECRET_KEY            = 'This string will be replaced with a proper key in production.'
SALT_ACCOUNT_ACTIVATE = 'This string will be replaced with a proper account activation salt in production.'
SALT_INVITE_ACTIVATE  = 'This string will be replaced with a proper invite activation salt in production.'


# When set to True, grabbled responses for all endpoint
# will be returned; default is False, obviously.
#
# This can also be set on service or endpoint. When it 
# is set on both the service and endpoint,
# the value from the endpoint is used.
HOT_FUZZ = False

# This will introduce a delay, in seconds, sending
# response forall endpoints. Default is 0.19 second,
# a delay of amount 186 milliseconds.
#
# This can also be set on service or endpoint. When it 
# is set on both the service and endpoint,
# the value from the endpoint is used.
RESPONSE_LAG = 0.19

DEBUG                       = True
PRODUCTION                  = not DEBUG
JSONIFY_PRETTYPRINT_REGULAR = False
CORS_ENABLED                = False
CORS_ALLOWED_ORIGINS        = (
    #'http://localhost:9294', # Exact String Compare
    #re.compile("^http([s]*):\/\/localhost([\:\d]*)$"), # Match a regex
)

# Mail server
MAIL_SERVER             = "localhost"
MAIL_PORT               = 465
MAIL_USE_TLS            = False
MAIL_USE_SSL            = True
MAIL_DEBUG              = DEBUG
MAIL_USERNAME           = "support@exmaple.com"
MAIL_DEFAULT_SENDER     = "support@example.com"
MAIL_MAX_EMAILS         = 10
MAIL_SUPPRESS_SEND      = False
MAIL_ASCII_ATTACHMENTS  = False
