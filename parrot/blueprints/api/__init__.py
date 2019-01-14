# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint
from .     import constants as API

bp_api_config = Blueprint('bp_api_config', __name__, url_prefix=f'{API.VERSION_URL}/manage')
bp_api        = Blueprint('bp_api', __name__, url_prefix='/api')

# Import the modules containing the view functions down here so these
# modules can import the blueprint from here
from . import home   # noqa
from . import configuration # noqa
