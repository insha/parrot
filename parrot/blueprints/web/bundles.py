# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2020 by Farhan Ahmed.
    :license: See LICENSE for more details.
"""

from flask import current_app, render_template

from parrot.blueprints.api import constants as API
from parrot.core.service import load_service_config
from . import BP_WEB


@BP_WEB.route("/bundle/<bundle_name>/doc", methods=["GET"])
def bundle_doc(bundle_name):
    template = "bundle_doc.html"

    if bundle_name:
        service = load_service_config(current_app, bundle_name)
    else:
        # Nothing to do.
        pass

    return render_template(
        template, service=service, default_lag=API.DEFAULT_RESPONSE_LAG
    )
