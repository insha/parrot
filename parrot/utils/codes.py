# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

import random
import string

RANDOM_CODE_KIND_ALL     = 'all'
RANDOM_CODE_KIND_LETTERS = 'letters'
RANDOM_CODE_KIND_NUMBERS = 'numbers'

def get_random_code(kind=RANDOM_CODE_KIND_ALL, length=10):
    selected_kind = kind.lower()
    
    if selected_kind == RANDOM_CODE_KIND_LETTERS:
        code = ''.join(random.choice(string.ascii_letters) for x in range(length))
    elif selected_kind == RANDOM_CODE_KIND_NUMBERS:
        code = ''.join(random.choice(string.digits) for x in range(length))
    else:
        code = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(length))
    
    return code
