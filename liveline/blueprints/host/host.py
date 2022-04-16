from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
    make_response,
)
from liveline.logger import logger
from liveline.presentation import slide, widget, presentation
from liveline.presentation.slides import TitleSlide
from liveline.database import PRESENTATION_PATH, database
from dataclasses import asdict
from werkzeug.utils import secure_filename

import uuid
import flask_login

host = Blueprint("host", __name__, static_folder="static", template_folder="templates")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "svg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@host.route("/presentation_creator", methods=["GET", "POST"])
@flask_login.login_required
def presentation_creator():
    return render_template("host/presentation_creator.html")


@host.route("/presentation_creator_confirm", methods=["GET", "POST"])
@flask_login.login_required
def presentation_creator_confirm():
    if request.method == "POST":
        return create_presentation_internal(request.form["presentation_name"])
    return render_template("host/presentation_creator_confirmation.html")
    return redirect(url_for("host.presentation_creator"))


def create_presentation_internal(name: str):
    flask_login.current_user.presentations.append(
        presentation.Presentation([], str(name), str(uuid.uuid4()))
    )
    database.commit()
    return redirect(url_for("host.presentation_creator"))

@host.route('/present/<id>')
def present(id):
    return render_template('host/presentation.html')