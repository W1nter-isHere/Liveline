from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
    make_response,
    flash
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
    return render_template("viewer/presentation_slides.html", room_code=room_code)

@viewer.route("/<room_code>.json")
def get_pres_json(room_code):
    print("requested data with room code")
    try:
        room = database.get_room(room_code)
        print(room)
        pres = database.get_presentation(room.presentation)
        print(pres)
        return jsonify(asdict(pres))
    except (RoomNotFoundException, PresentationNotFoundException):
        return jsonify({})

@viewer.route("/id/<id>.json")
def get_pres_json_with_id(id):
    try:
        pres = database.get_presentation(id)
        return jsonify(asdict(pres))
    except PresentationNotFoundException:
        return jsonify({})

@viewer.route("/join_presentation", methods=["GET", "POST"])
def join_presentation():
    if request.method == "POST":
        if not database.has_room(request.form["room_code"]):
            flash("Room code is invalid", "error")
            return redirect(url_for("viewer.join_presentation"))
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
