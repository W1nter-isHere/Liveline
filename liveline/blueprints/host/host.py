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
from liveline.presentation import presentation, slides
from liveline.presentation.slides import TitleSlide
from liveline.database import PRESENTATION_PATH, database, PresentationNotFoundException
from dataclasses import asdict
from werkzeug.utils import secure_filename

import uuid
import flask_login

host = Blueprint("host", __name__, static_folder="static", template_folder="templates")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "svg"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@host.route("/presentation_creator/<id>")
@flask_login.login_required
def presentation_creator(id):
    return render_template("host/presentation_creator.html", id=id)


@host.route("/presentation_creator/<id>/delete_slide/<index>")
def delele_slide(id, index):
    try:
        pres = database.get_presentation(id)
        if len(pres.slides) - 1 < 0:
            return ("Slide is empty!", 404)
        pres.slides.pop(int(index))
        database.commit()
    except PresentationNotFoundException:
        return ("Presentation not found", 404)
    return ("", 200)

@host.route("/presentation_creator/<id>/add_slide/<typ>")
def add_slide(id, typ):
    try:
        s = database.get_presentation(id).slides
        if typ == "TitleSlide":
            s.append(slides.TEMPLATE_TITLE)
        elif typ == "TextSlide":
            s.append(slides.TEMPLATE_TEXT)
        elif typ == "ImageSlide":
            s.append(slides.TEMPLATE_IMAGE)
        database.commit()
    except PresentationNotFoundException:
        return ("Presentation not found", 404)

    return ("", 200)


@host.route("/presentation_creator_confirm", methods=["GET", "POST"])
@flask_login.login_required
def presentation_creator_confirm():
    if request.method == "POST":
        return create_presentation_internal(request.form["presentation_name"])
    return render_template("host/presentation_creator_confirmation.html")


def create_presentation_internal(name: str):
    pres = presentation.Presentation(
        [], str(name), str(uuid.uuid4()), str(flask_login.current_user.id)
    )
    flask_login.current_user.presentations.append(pres.identifier)
    database.add_presentation(pres)
    database.commit()
    return redirect(url_for("host.presentation_creator", id=pres.identifier))


@host.route("/present/<id>")
def present(id):
    return render_template("host/presentation.html", id=id)
