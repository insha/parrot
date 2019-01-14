# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

import pytest

from parrot.utils.codes import get_random_code

class TestRandomCode(object):
    def test_code_length(self):
        code = get_random_code(kind='all', length=10)
        assert len(code) == 10

    def test_code_type_numeric(self):
        code = get_random_code(kind='numbers', length=5)
        assert len(code) == 5

    def test_code_type_letters(self):
        code = get_random_code(kind='letters', length=5)
        assert len(code) == 5
