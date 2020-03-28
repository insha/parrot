# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2020 by Farhan Ahmed.
    :license: See LICENSE for more details.
"""

from flask import Blueprint
from parrot.blueprints.api import constants as API

BP_WEB = Blueprint("bp_web", __name__, url_prefix="", template_folder="templates")

# pylint: disable=wrong-import-position
from . import home  # noqa
from . import bundles  # noqa

# pylint: enable=wrong-import-position
