# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

# XXX: Never import this package. It only exists so the `flask`
# command can use it (using `FLASK_APP=parrot._cliapp`) as it cannot
# use an app factory directly

from parrot.core.app import create_app

app = create_app()
