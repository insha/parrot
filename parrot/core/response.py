# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2020 by Farhan Ahmed.
    :license: See LICENSE for more details.
"""
import time

from flask import jsonify, current_app
from parrot.blueprints.api import constants as API
from parrot.blueprints.api.errors import bundle as BUNDLE_ERROR
from parrot.utils.codes import get_random_code


class ParrotResponse:
    def __init__(self, **kwargs):
        self.status_code = kwargs.get("status_code", API.HTTP_STATUS_CODE_OK)
        self.error_code = kwargs.get("error_code", API.RESPONSE_RESULT_SUCCESS)
        self.message = kwargs.get("message", None)
        self.content = kwargs.get("content", None)
        self.errors = kwargs.get("errors", None)
        self.lag = kwargs.get("lag", 0)
        self.fuzz = kwargs.get("fuzz", False)
        self.headers = kwargs.get("headers", {"content-type": "application/json"})

    def __repr__(self):
        return "<%s %r (%r)>" % (self.__class__.__name__, self.content, self.error_code)

    def _to_json(self, status_code=API.HTTP_STATUS_CODE_OK):
        template = {}

        if self.content:
            template = self.content

        if self.error_code != API.RESPONSE_RESULT_SUCCESS:
            template[API.RESPONSE_ERROR_KEY] = {
                API.RESPONSE_ERROR_CODE_KEY: self.error_code,
                API.RESPONSE_MESSAGE_KEY: self.message
                or BUNDLE_ERROR.MESSAGES[BUNDLE_ERROR.NOT_FOUND],
            }

            if self.errors:
                template[API.RESPONSE_ERROR_KEY][
                    API.RESPONSE_ERROR_LIST_KEY
                ] = self.errors

        json_response = jsonify(template)
        json_response.status_code = status_code

        return json_response

    def generate_response(self):
        prepared_response = None

        if current_app.config["HOT_FUZZ"]:
            fuzzed_payload = get_random_code(kind="all", length=256)
            prepared_response = fuzzed_payload, self.status_code

            current_app.logger.debug(
                f"Fuzzed Response:\n({self.status_code}) {fuzzed_payload}"
            )
        else:
            prepared_response = self._to_json(status_code=self.status_code)

        if current_app.config["RESPONSE_LAG"] > 0:
            lag = current_app.config["RESPONSE_LAG"]

            time.sleep(lag)

        return prepared_response
