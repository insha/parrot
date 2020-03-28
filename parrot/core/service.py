# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2020 by Farhan Ahmed.
    :license: See LICENSE for more details.
"""

import os
import uuid

from json import JSONDecodeError
from flask import current_app, json
from parrot.core.endpoint import ServiceEndpoint
from parrot.core.response import ParrotResponse
from parrot.blueprints.api import constants as API


class Service:
    name = None
    base_url = None
    lag = 0
    fuzz = False
    # Dictionary where the `key` is the api endpoint (url) and the value is an instance of ServiceEndpoint
    endpoints = {}
    description = ""
    identifier = None

    def __init__(self, **kwargs):
        super(Service, self).__init__(**kwargs)

        self.name = kwargs.get("name", API.DEFAULT_SERVICE_NAME)
        self.base_url = kwargs.get("base_url", None)
        self.endpoints = kwargs.get("endpoints", {})
        self.description = kwargs.get("description", "")
        self.identifier = kwargs.get("identifier", str(uuid.uuid1()))

    def __repr__(self):
        return f"<Service {hex(id(self))}> {self.name} {self.identifier}"

    def load_bundle(self, name=None):
        """Loads a bundle with the provided `name` from the file system.

        :param name: Name of the bundle.
        """
        if name:
            self.reset()

            new_service = load_service_config(current_app, bundle_name=name)

            for field_name, field_value in new_service.__dict__.items():
                if hasattr(self, field_name):
                    setattr(self, field_name, field_value)
        else:
            # Nothing to do.
            pass

    def find(self, method=None, endpoint=None, parameters=None):
        """Lookup the endpoint with the provided information.

        :param method:     The HTTP method for an endpoint.
        :param endpoint:   The path of the endpoint.
        :param parameters: The query parameters for an endpoint, if any.

        :returns: An instance of the :class:`ServiceResponse`. The `error_code`
                  will be set when an endpoint is not found.
        """
        response = None

        try:
            api_endpoint = self._find_endpoint(key=endpoint, parameters=parameters)

            if api_endpoint:
                response = api_endpoint.responses[method.upper()]
        except KeyError as _:
            message = f"Could not find a matching endpoint: ({method}) {endpoint} {parameters}"
            response = ParrotResponse()
            response.status_code = API.HTTP_STATUS_CODE_NOT_FOUND
            response.headers = {"content-type": "application/json"}
            response.message = message
            response.error_code = -20001

        return response

    def _find_endpoint(self, key=None, parameters=None):
        """This is a private method that is invoked by the public
        `find` method of :class:`Service`.

        :param key:        The path of an endpoint.
        :param parameters: The query parameters for an endpoint, if any.

        :returns: An instance of the :class:`ServiceEndpoint` when successful.
                  None when an endpoint could not be matched.
        """
        api_endpoint = None  # This is of type ServiceEndpoint

        try:
            api_endpoint = self.endpoints[key]

            if parameters:
                # When query string parameters are provided for an
                # endpoint, they will be matched.
                did_match_parameters = api_endpoint.parameters == parameters.to_dict()

                if not did_match_parameters:
                    api_endpoint = None
        except KeyError as _:
            pass

        return api_endpoint

    def update(self, payload=None):
        """This is used for updating an already existing endpoint.

        :param payload: A dict with information about the endpoint that is being updated.
        """
        did_update = False
        message = None
        endpoint = payload.get(API.RESPONSE_PAYLOAD_ENDPOINT_KEY)
        method = payload.get(API.RESPONSE_PAYLOAD_METHOD_KEY)
        parameters = payload.get(API.RESPONSE_PAYLOAD_PARAMETERS_KEY, None)
        service_endpoint = self.find(
            method=method, endpoint=endpoint, parameters=parameters
        )

        if service_endpoint.error_code == 0:
            service_endpoint.method = method
            service_endpoint.content = payload.get(API.RESPONSE_PAYLOAD_CONTENT_KEY)

            self.endpoints[endpoint].responses[method.upper()] = service_endpoint

            did_update = True
        else:
            message = service_endpoint.message

        return (did_update, message)

    def add_endpoint(self, endpoint):
        """Adds an endpoint to a service.

        :param payload: A dict containing information for the endpoint that will be added.
        """
        did_add = False
        message = None

        self.endpoints[endpoint.url] = endpoint

        return (did_add, message)

    def remove(self, payload=None):
        did_remove = False
        message = None
        key = payload.get(API.RESPONSE_PAYLOAD_ENDPOINT_KEY, None)
        method = payload.get(API.RESPONSE_PAYLOAD_METHOD_KEY, None)
        parameters = payload.get(API.RESPONSE_PAYLOAD_PARAMETERS_KEY, None)

        try:
            if method is None and parameters is None:
                self.endpoints.pop(key)
            else:
                endpoint = self._find_endpoint(key=key, parameters=parameters)
                endpoint.responses.pop(method)

            did_remove = True
        except KeyError as _:
            message = f"Could not remove endpoint `{endpoint}`"

        return (did_remove, message)

    def reset(self):
        """This will remove all endpoints and all configuration
        for a service; essentially a 'reset to factory setting'
        method.

        NOTE: This will always return `True`.
        """
        self.name = API.DEFAULT_SERVICE_NAME
        self.base_url = None
        self.endpoints = {}
        self.lag = 0
        self.fuzz = False

        return True

    def info(self, app_info=None):
        """Generates information about all of the endpoints for a service.

        :param app_info: version and copyright information about the app.
        """
        payload = {
            "name": self.name,
            "lag": self.lag,
            "fuzz": self.fuzz,
            "description": self.description,
        }
        service_endpoints = []

        # `url` == the api endpoint and the endpoint is an instance of ServiceEndpoint
        for url, endpoint in self.endpoints.items():
            service_responses = []

            for method, response in endpoint.responses.items():
                service_responses.append(
                    {
                        API.RESPONSE_PAYLOAD_METHOD_KEY: method,
                        API.RESPONSE_PAYLOAD_STATUS_CODE_KEY: response.status_code,
                        API.RESPONSE_PAYLOAD_HEADERS_KEY: response.headers,
                        API.RESPONSE_PAYLOAD_CONTENT_KEY: response.content,
                        API.RESPONSE_PAYLOAD_LAG_KEY: response.lag,
                        API.RESPONSE_PAYLOAD_FUZZ_KEY: response.fuzz,
                    }
                )

            service_endpoints.append(
                {
                    API.CONFIGURATION_URL_KEY: url,
                    API.CONFIGURATION_DESCRIPTION_KEY: endpoint.description,
                    API.RESPONSE_PAYLOAD_PARAMETERS_KEY: endpoint.parameters,
                    API.CONFIGURATION_RESPONSES_KEY: service_responses,
                }
            )

        payload[API.CONFIGURATION_ENDPOINTS_KEY] = service_endpoints

        if app_info:
            payload[
                "version"
            ] = f"{app_info.name} {app_info.version} ({app_info.build})"
            payload["copyright"] = f"{app_info.copyright}"

        payload[API.CONFIGURATION_IDENTIFIER_KEY] = self.identifier

        info_response = ParrotResponse()
        info_response.content = payload

        return info_response


def load_service_config(app=None, bundle_name=None):
    """This method will load a configuration from the file system, and then
    parse the information and create a instance of the :class:`Service`
    from the parsed information.

    :param app:         The current Flask app that is running.
    :param bundle_name: Name of the bundle that will be loaded.
    """
    service = None
    json_path = None
    config = bundle_name
    config_filename = app.config.get("CONFIGURATION_FILE_NAME", None)
    config_path = app.config.get("CONFIG_PATH", None)
    responses_folder = app.config.get("RESPONSES_FOLDER", None)

    if config:
        with app.app_context():
            try:
                bundle = os.path.join(config_path, config)
                json_path = os.path.join(bundle, config_filename)
                data = json.load(open(json_path))
                service = _parse_bundle(
                    config=config,
                    data=data,
                    config_path=config_path,
                    responses_folder=responses_folder,
                )
            except JSONDecodeError as invalid_json_error:
                error_message = (
                    f"Provided JSON is invalid.\n"
                    f"---------------------------"
                    f"{invalid_json_error.msg}"
                    f"---------------------------"
                    f"Document: {invalid_json_error.doc}"
                    f"Position: {invalid_json_error.pos}"
                    f"Line    : {invalid_json_error.lineno}"
                )
                current_app.logger.error(error_message)
            except OSError as error:
                error_message = f"Could not load the configuration for `{config}`. ({json_path})\n{error}"
                current_app.logger.info(error_message)
    else:
        service = Service()
        service.name = API.DEFAULT_SERVICE_NAME

    return service


def _parse_bundle(config=None, data=None, config_path=None, responses_folder=None):
    """This is a private(internal) method for parsing a bundle that read from the file system.

    :param config:           The application configuration for bundle location.
    :param data:             The data that has been loaded and parsed as JSON for the bundle.
    :param config_path:      The path to the bundle configuration file.
    :param responses_folder: The name of the folder that holds the responses for a bundle.
    """
    service = Service()
    service.name = data.get(API.CONFIGURATION_NAME_KEY)
    service.base_url = data.get(API.CONFIGURATION_BASE_URL_KEY, None)
    service.description = data.get(API.CONFIGURATION_DESCRIPTION_KEY, "")
    endpoint_configs = data.get(API.CONFIGURATION_ENDPOINTS_KEY, [])

    if len(endpoint_configs) == 0:
        current_app.logger.info(
            "{name} does not have any endpoints.".format(name=service.name)
        )
    else:
        endpoint = ServiceEndpoint()

        for endpoint_config in endpoint_configs:
            endpoint.description = endpoint_config.get(
                API.CONFIGURATION_DESCRIPTION_KEY, ""
            )
            endpoint.url = endpoint_config.get(API.CONFIGURATION_URL_KEY)
            endpoint.parameters = endpoint_config.get(
                API.RESPONSE_PAYLOAD_PARAMETERS_KEY, None
            )
            endpoint_responses = endpoint_config.get(
                API.CONFIGURATION_RESPONSES_KEY, {}
            )

            for method, content in endpoint_responses.items():
                try:
                    status_code = content.get(API.RESPONSE_PAYLOAD_STATUS_CODE_KEY, 200)
                    content_file = content.get(API.CONFIGURATION_CONTENT_KEY, None)
                    response_body = None

                    if status_code != 204 and (
                        content_file is None or len(content_file) == 0
                    ):
                        raise ValueError(
                            "The value of the `content` node is invalid for `status_code` of `%d`"
                            % status_code
                        )

                    if status_code != 204:
                        # There should not be any content associated with a response
                        # when the HTTP status code is 204. Therefore we are not going
                        # to bother loading anything from the `content` node.
                        json_path = os.path.join(
                            config_path, config, responses_folder, content_file
                        )
                        data = json.load(open(json_path))
                        response_body = data

                    payload = {
                        API.RESPONSE_PAYLOAD_METHOD_KEY: method.upper(),
                        API.RESPONSE_PAYLOAD_STATUS_CODE_KEY: status_code,
                        API.RESPONSE_PAYLOAD_HEADERS_KEY: content.get(
                            API.RESPONSE_PAYLOAD_HEADERS_KEY, API.DEFAULT_HEADER
                        ),
                        API.RESPONSE_PAYLOAD_CONTENT_KEY: response_body,
                        API.RESPONSE_PAYLOAD_LAG_KEY: content.get(
                            API.RESPONSE_PAYLOAD_LAG_KEY, API.DEFAULT_RESPONSE_LAG
                        ),
                        API.RESPONSE_PAYLOAD_FUZZ_KEY: content.get(
                            API.RESPONSE_PAYLOAD_FUZZ_KEY, False
                        ),
                    }

                    endpoint.add_response(payload=payload)
                except ValueError as error:
                    error_message = (
                        f"Could not load the response for endpoint `{endpoint.url}`"
                        f" from file `{content_file}`. {error}"
                    )
                    current_app.logger.info(error_message)

            service.add_endpoint(endpoint=endpoint)

    return service


class Services:
    def __init__(self):
        self._items = {}

    def find(self, identifier):
        service = None  # This is of type Service

        try:
            service = self._items[identifier]
        except KeyError as _:
            pass

        return service

    def add(self, service=Service()):
        service_exists = self.find(service.identifier)

        if not service_exists:
            self._items[service.identifier] = service
        else:
            pass

        return service

    def clear(self):
        self._items = {}


SERVICES = Services()
