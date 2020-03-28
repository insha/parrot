# -*- coding: utf-8 -*-
"""
    :copyright: © 2010-2020 by Farhan Ahmed.
    :license: See LICENSE for more details.
"""

from flask import request, current_app, send_from_directory, render_template
from flask_mail import Message
from parrot.blueprints.api import constants as API
from parrot.core.mail import MAIL
from . import BP_WEB


@BP_WEB.route("/favicon", methods=["GET"])
def favicon():
    return send_from_directory(
        "static", "images/favicon.ico", mimetype="image/vnd.microsoft.icon"
    )


@BP_WEB.route("/", methods=["GET"])
def homepage():
    return render_template("home.html"), API.HTTP_STATUS_CODE_OK


@BP_WEB.route("/about", methods=["GET"])
def about():
    return render_template("about.html"), API.HTTP_STATUS_CODE_OK


@BP_WEB.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html"), API.HTTP_STATUS_CODE_OK


@BP_WEB.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html"), API.HTTP_STATUS_CODE_OK


@BP_WEB.route("/terms", methods=["GET"])
def terms():
    return render_template("terms.html"), API.HTTP_STATUS_CODE_OK


@BP_WEB.route("/docs/guide", methods=["GET"])
def docs_guide():
    return render_template("docs_guide.html"), API.HTTP_STATUS_CODE_OK


@BP_WEB.route("/docs/manage", methods=["GET"])
def docs_manage():
    return render_template("docs_manage.html"), API.HTTP_STATUS_CODE_OK


@BP_WEB.route("/feedback", methods=["POST"])
def feedback():
    message = request.form.get("message", None)
    heading = "Thank you"
    result = True

    if message:
        send_feedback_email(message)
    else:
        heading = "Oops"
        result = False
        current_app.logger.debug("Nothing was sent in the message.")

    return (
        render_template(
            "feedback.html", result=result, heading=heading, message=message
        ),
        API.HTTP_STATUS_CODE_OK,
    )


def send_feedback_email(body):
    if body:
        message = Message(
            subject="Parrot Feedback", recipients=["parrot.support@themacronaut.com"]
        )
        message.body = body

        MAIL.send(message)
    else:
        current_app.logger.debug("A message is required for sending the email.")
