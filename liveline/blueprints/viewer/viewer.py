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
from liveline.presentation.slides import TextSlide, ImageSlide
from liveline.database import database, RoomNotFoundException, PresentationNotFoundException
from dataclasses import asdict

import flask_login
import uuid

viewer = Blueprint(
    "viewer", __name__, static_folder="static", template_folder="templates"
)

@viewer.route("/<room_code>")
def viewer_screen(room_code):
    if not database.has_room(room_code):
        return redirect(url_for("profile.profile_page"))
    return render_template("viewer/presentation_slides.html", room_code=room_code)

@viewer.route("/<room_code>.json")
def get_pres_json(room_code):
    # try:
    #     room = database.get_room(room_code)
    #     pres = database.get_presentation(room.presentation)
    #     return jsonify(asdict(pres))
    # except (RoomNotFoundException, PresentationNotFoundException):
    #     return jsonify({})

    pres = presentation.Presentation(
        [
            TextSlide("AHHH", "YOOOOOOOOOOOOOOOOOOOOOO", None),
            TextSlide("53152", "YOOOOOOOOOOOOOOOOOOOOOO", None),
            TextSlide("12131", "YOOOOOOOOOOOOOOOOOOOOOO", None),
            TextSlide("3254", "YOOOOOOOOOOOOOOOOOOOOOO", None),
            TextSlide("65", "YOOOOOOOOOOOOOOOOOOOOOO", None)
        ],
        "Test Slide",
        str(uuid.uuid4()),
        str(uuid.uuid4())
    )
    return jsonify(asdict(pres))

@viewer.route("/id/<id>.json")
def get_pres_json_with_id(id):
    # try:
    #     pres = database.get_presentation(id)
    #     return jsonify(asdict(pres))
    # except PresentationNotFoundException:
    #     return jsonify({})

    pres = presentation.Presentation(
        [
            TextSlide("AHHH", "YOOOOOOOOOOOOOOOOOOOOOO", None),
            TextSlide("53152", "YOOOOOOOOOOOOOOOOOOOOOO", None),
            TextSlide("12131", "YOOOOOOOOOOOOOOOOOOOOOO", None),
            TextSlide("3254", "YOOOOOOOOOOOOOOOOOOOOOO", None),
            TextSlide("65", "YOOOOOOOOOOOOOOOOOOOOOO", None)
        ],
        "Test Slide",
        str(uuid.uuid4()),
        str(uuid.uuid4())
    )

    print(asdict(pres))

    return jsonify(asdict(pres))

@viewer.route("/join_presentation", methods=["GET", "POST"])
def join_presentation():
    if request.method == "POST":
        return redirect(url_for("viewer.viewer_screen", room_code=request.form["room_code"]))
    return render_template("viewer/join_presentation.html")

# @viewer.route("/widget_based/<id>")
# @flask_login.login_required
# def test(id):
#     return render_template("viewer/presentation_widgets.html", id=id)


# @viewer.route("/widget_based/<id>/slide")
# @flask_login.login_required
# def slide_test(id):
#     test = slide.Slide(
#         [slide.Widget("THE", widget.TEXT_WIDGET, (80, 200))],
#         "/static/resources/logo.svg",
#     )
#     return jsonify(asdict(test))
