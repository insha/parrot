# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

from flask import Blueprint
from parrot.blueprints.api import constants as API

bp_web = Blueprint('bp_web', __name__, url_prefix='', template_folder='templates')

from . import home # noqa
from . import bundles # noqa