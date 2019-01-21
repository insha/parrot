# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

import time

from copy import deepcopy
from flask import g, session, request, current_app

from . import constants as API
from . import bp_api
from parrot.utils.codes import get_random_code, RANDOM_CODE_KIND_ALL


@bp_api.route("/", defaults={"path": ""}, methods=API.ALLOWED_METHODS)
@bp_api.route("/<path:path>", methods=API.ALLOWED_METHODS)
def catch_all(path):
    parameters = request.args
    response = deepcopy(
        g.service.find(method=request.method, endpoint=path, parameters=parameters)
    )
    response_lag = response.lag if response.lag > 0 else g.service.lag
    response_fuzz = response.fuzz if response.fuzz else g.service.fuzz

    if response_lag > 0:
        time.sleep(response_lag)

    if response_fuzz:
        response.content = get_random_code(kind=RANDOM_CODE_KIND_ALL, length=256)

    return response
