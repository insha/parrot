# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2020 by Farhan Ahmed.
    :license: See LICENSE for more details.
"""

from flask import Blueprint
from . import constants as API

BP_API_CONFIG = Blueprint(
    "bp_api_config", __name__, url_prefix=f"{API.VERSION_URL}/manage"
)
BP_API = Blueprint("bp_api", __name__, url_prefix="/api")

# Import the modules containing the view functions down here so these
# modules can import the blueprint from here
# pylint: disable=wrong-import-position
from . import home  # noqa
from . import configuration  # noqa

# pylint: enable=wrong-import-position
