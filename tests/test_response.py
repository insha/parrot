# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

import pytest

from parrot.core.app import create_app
from parrot.blueprints.api import constants as API
from parrot.blueprints.api.errors import configuration as CONFIG_ERROR

@pytest.fixture
def client():
    return create_app().test_client()

def test_success_response(client):
    response = client.get('/1/manage/', follow_redirects=True)
    json_data = response.get_json()
    
    assert response.status_code == API.HTTP_STATUS_CODE_NOT_FOUND
    assert json_data is not None

def test_error_response(client):
    response = client.post('/1/manage/', json={}, follow_redirects=True)
    json_data = response.get_json()
    
    assert response.status_code == API.HTTP_STATUS_CODE_BAD_REQUEST
    assert json_data.get(API.RESPONSE_ERROR_KEY, None) is not None
    assert json_data[API.RESPONSE_ERROR_KEY][API.RESPONSE_ERROR_CODE_KEY] == CONFIG_ERROR.INVALID_DATA
    assert json_data[API.RESPONSE_ERROR_KEY][API.RESPONSE_MESSAGE_KEY] is not None
