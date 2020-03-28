# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2020 by Farhan Ahmed.
    :license: See LICENSE for more details.
"""

import pytest

from parrot.core.app import create_app
from parrot.blueprints.api import constants as API


@pytest.fixture
def client():
    return create_app().test_client()


class TestServiceClass(object):
    def test_default_service(self, client):
        configure_service = client.post("/1/manage/bundle/empty", follow_redirects=True)
        response = client.get("/1/manage/", follow_redirects=True)
        json_data = response.get_json()

        assert configure_service.status_code == API.HTTP_STATUS_CODE_NO_CONTENT
        assert response.status_code == API.HTTP_STATUS_CODE_OK
        assert json_data[API.CONFIGURATION_NAME_KEY] == API.DEFAULT_SERVICE_NAME
        assert json_data[API.CONFIGURATION_ENDPOINTS_KEY] == []

    def test_loading_bundle_successfully(self, client):
        response = client.put("/1/manage/bundle/movies")

        assert response.status_code == API.HTTP_STATUS_CODE_NO_CONTENT

    def test_find_endpoint_success(self, client):
        configure_service = client.put("/1/manage/bundle/movies")
        response = client.get("/api/movies")
        json_data = response.get_json()

        assert configure_service.status_code == API.HTTP_STATUS_CODE_NO_CONTENT
        assert response.status_code == API.HTTP_STATUS_CODE_OK
        assert len(json_data) > 0

    def test_find_endpoint_failure(self, client):
        setup_service = client.put("/1/manage/bundle/movies")
        response = client.get("/api/stars-wars")
        json_data = response.get_json()

        assert setup_service.status_code == API.HTTP_STATUS_CODE_NO_CONTENT
        assert response.status_code == API.HTTP_STATUS_CODE_NOT_FOUND
        assert json_data[API.RESPONSE_ERROR_KEY][API.RESPONSE_ERROR_CODE_KEY] == -1001
        assert json_data[API.RESPONSE_ERROR_KEY][API.RESPONSE_MESSAGE_KEY] is not None
