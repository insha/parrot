# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

COULD_NOT_ADD_ENDPOINT = -2001
COULD_NOT_UPDATE_ENDPOINT = -2002
COULD_NOT_RESET_ENDPOINT = -2003
INVALID_DATA = -2004
NO_SERVICE_AVAILABLE = -2005

MESSAGES = {
    COULD_NOT_ADD_ENDPOINT: 'Could not add endpoint `{}`',
    COULD_NOT_UPDATE_ENDPOINT: 'Could not update endpoint `{}`',
    COULD_NOT_RESET_ENDPOINT: 'Could not reset service `{}`',
    INVALID_DATA: 'The provided information is invalid.',
    NO_SERVICE_AVAILABLE: 'No service has been created. Thus, no information is available.',
}
