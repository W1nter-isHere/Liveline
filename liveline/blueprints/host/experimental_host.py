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
    # if request.method == "POST":
    #     if "presentation" not in request.files:
    #         return redirect(request.url)

    #     raw_presentation = request.files["presentation"]

    #     if allowed_file(raw_presentation.filename):
    #         presentation_path = (
    #             PRESENTATION_PATH
    #             + flask_login.current_user.id
    #             + "."
    #             + secure_filename(raw_presentation.filename).rsplit(".", 1)[1].lower()
    #         )
    #         raw_presentation.save("liveline/" + presentation_path)
    #         flask_login.current_user.presentation_path = presentation_path
    #         database.get_user(flask_login.current_user.id).presentation_path = presentation_path
    #         database.commit()
    #         return redirect(url_for("profile.profile_page"))

    return render_template("host/presentation_creator.html")


@host.route("/presentation_creator_confirm", methods=["GET", "POST"])
@flask_login.login_required
def presentation_creator_confirm():
    if request.method == "POST":
        return create_presentation_internal(request.form["presentation_name"])
    return render_template("host/presentation_creator_confirmation.html")


def create_presentation_internal(name: str):
    flask_login.current_user.presentations.append(
        presentation.WidgetBasedPresentation([], name, str(uuid.uuid4()))
    )
    database.commit()
    return redirect(url_for("host.presentation_creator"))
