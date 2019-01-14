# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2019 by Farhan Ahmed.
    :license: BSD, see LICENSE for more details.
"""

from copy  import deepcopy
from flask import g, session, request, current_app, render_template, redirect, url_for

from .                            import bp_web
from parrot.blueprints.api        import constants as API
from parrot.blueprints.api.errors import bundle as BUNDLE_ERROR
from parrot.blueprints.api.errors import configuration as CONFIG_ERROR
from parrot.core.response         import ServiceResponse
from parrot.core.service          import load_service_config

@bp_web.route('/bundle/<bundle_name>/doc', methods=['GET'])
def bundle_doc(bundle_name):
    template = 'bundle_doc.html'
    
    if bundle_name:
        service = load_service_config(current_app, bundle_name)
    else:
        # Nothing to do.
        pass
    
    return render_template(template, service=service, default_lag=API.DEFAULT_RESPONSE_LAG)
