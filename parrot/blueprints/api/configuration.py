# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

from copy import deepcopy
from flask import g, session, request, current_app

from . import constants as API
from . import bp_api_config
from .errors import bundle as BUNDLE_ERROR
from .errors import configuration as CONFIG_ERROR
from parrot.core.response import ServiceResponse
from parrot.core.service import services, Service, load_service_config


@bp_api_config.route('/', methods=['GET'])
def info():
    response = ServiceResponse(status_code=API.HTTP_STATUS_CODE_OK)

    if not g.service:
        response.error_code = CONFIG_ERROR.NO_SERVICE_AVAILABLE
        response.message = CONFIG_ERROR.MESSAGES[CONFIG_ERROR.NO_SERVICE_AVAILABLE]
        response.status_code = API.HTTP_STATUS_CODE_NOT_FOUND
    else:
        response = g.service.info(app_info=g.app_info)

    return response


@bp_api_config.route('/', methods=['POST', 'PUT', 'DELETE'])
def manage_endpoint():
    response = None
    payload = request.get_json()
    payload_error = False if not payload and request.method == 'DELETE' else True

    if payload_error:
        response = ServiceResponse()
        response.status_code = API.HTTP_STATUS_CODE_BAD_REQUEST
        response.error_code = CONFIG_ERROR.INVALID_DATA
        response.message = CONFIG_ERROR.MESSAGES[CONFIG_ERROR.INVALID_DATA].format()
    else:
        if request.method == 'POST':
            response = add_endpoint(payload=payload)
        elif request.method == 'PUT':
            response = update_endpoint(payload=payload)
        else:
            response = reset_service()

    return response


@bp_api_config.route('/bundle/<bundle_name>', methods=['PUT', 'POST'])
def load_bundle(bundle_name):
    response = ServiceResponse(status_code=API.HTTP_STATUS_CODE_NO_CONTENT)

    if bundle_name:
        if request.method == 'POST':
            service = Service()
            g.service = services.add(service)
        else:
            if g.service:
                g.service.load_bundle(name=bundle_name)
            else:
                service = Service()
                service.load_bundle(name=bundle_name)
                g.service = services.add(service)

        if g.service is None:
            response.error_code = BUNDLE_ERROR.NOT_FOUND
            response.message = BUNDLE_ERROR.MESSAGES[BUNDLE_ERROR.NOT_FOUND].format(
                bundle_name
            )
            response.status_code = API.HTTP_STATUS_CODE_NOT_FOUND
        else:
            session[API.SESSION_USER_AUTHENTICATION_TOKEN_KEY] = g.service.identifier
    else:
        response.error_code = BUNDLE_ERROR.INVALID_REQUEST
        response.message = BUNDLE_ERROR.MESSAGES[BUNDLE_ERROR.INVALID_REQUEST]
        response.status_code = API.HTTP_STATUS_CODE_BAD_REQUEST

    return response


@bp_api_config.route('/bundle/<bundle_name>', methods=['GET'])
def bundle_information(bundle_name):
    response = ServiceResponse(status_code=API.HTTP_STATUS_CODE_OK)

    if bundle_name:
        service = load_service_config(current_app, bundle_name=bundle_name)
        response = service.info(app_info=g.app_info)
    else:
        response.error_code = BUNDLE_ERROR.INVALID_REQUEST
        response.message = BUNDLE_ERROR.MESSAGES[BUNDLE_ERROR.INVALID_REQUEST]
        response.status_code = API.HTTP_STATUS_CODE_BAD_REQUEST

    return response


def update_endpoint(payload=None):
    did_update, reason = g.service.update(payload=payload)
    response = ServiceResponse()
    response.headers = API.DEFAULT_HEADER
    response.status_code = (
        API.HTTP_STATUS_CODE_NO_CONTENT if did_update else API.HTTP_STATUS_CODE_OK
    )
    response.error_code = (
        API.RESPONSE_RESULT_SUCCESS
        if did_update
        else CONFIG_ERROR.COULD_NOT_UPDATE_ENDPOINT
    )
    response.message = None if did_update else reason

    return response


def add_endpoint(payload=None):
    did_add, reason = g.service.add_endpoint(payload=payload)
    response = ServiceResponse()
    response.headers = API.DEFAULT_HEADER
    response.status_code = (
        API.HTTP_STATUS_CODE_NO_CONTENT if did_add else API.HTTP_STATUS_CODE_OK
    )
    response.error_code = (
        API.RESPONSE_RESULT_SUCCESS if did_add else CONFIG_ERROR.COULD_NOT_ADD_ENDPOINT
    )
    response.message = None if did_add else reason

    return response


def reset_service():
    did_reset = g.service.reset()
    response = ServiceResponse()
    response.headers = API.DEFAULT_HEADER
    response.status_code = (
        API.HTTP_STATUS_CODE_NO_CONTENT
        if did_reset
        else API.HTTP_STATUS_CODE_INTERNAL_SERVER_ERROR
    )

    return response
