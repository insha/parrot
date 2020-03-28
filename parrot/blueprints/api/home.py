# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2020 by Farhan Ahmed.
    :license: See LICENSE for more details.
"""

import time

from copy import deepcopy
from flask import g, request
from parrot.utils.codes import get_random_code, RANDOM_CODE_KIND_ALL
from parrot.core.response import ParrotResponse
from . import constants as API
from . import BP_API
from .errors import bundle as BUNDLE_ERROR


@BP_API.route("/", defaults={"path": ""}, methods=API.ALLOWED_METHODS)
@BP_API.route("/<path:path>", methods=API.ALLOWED_METHODS)
def catch_all(path):
    parameters = request.args
    response = deepcopy(
        g.service.find(method=request.method, endpoint=path, parameters=parameters)
    )

    if response:
        response_lag = response.lag if response.lag > 0 else g.service.lag
        response_fuzz = response.fuzz if response.fuzz else g.service.fuzz

        if response_lag > 0:
            time.sleep(response_lag)

        if response_fuzz:
            response.content = get_random_code(kind=RANDOM_CODE_KIND_ALL, length=256)
    else:
        response = ParrotResponse(
            status_code=API.HTTP_STATUS_CODE_NOT_FOUND,
            error_code=BUNDLE_ERROR.NOT_FOUND,
        )

    return response
