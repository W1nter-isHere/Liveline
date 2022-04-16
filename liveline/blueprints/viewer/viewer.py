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
from liveline.database import database, RoomNotFoundException
from dataclasses import asdict

import flask_login
import uuid

viewer = Blueprint(
    "viewer", __name__, static_folder="static", template_folder="templates"
)


@viewer.route("/<id>")
def viewer_screen(id):
    # pres = presentation.Presentation()
    return render_template("viewer/presentation_slides.html", background="test.background", id=id)

@viewer.route("/<id>.json")
def get_pres_json(id):
    #'https://raster.repl.co/static/images/rasterlogo2021.png'
    if id == "1":
        pres = presentation.Presentation(
            [
                ImageSlide(
                    "Hallo",
                    [
                        "https://raster.repl.co/static/images/rasterlogo2021.png",
                        "https://raster.repl.co/static/images/rasterlogo2021.png",
                        "https://raster.repl.co/static/images/rasterlogo2021.png",
                        "https://raster.repl.co/static/images/rasterlogo2021.png",
                        "https://raster.repl.co/static/images/rasterlogo2021.png",
                        "https://raster.repl.co/static/images/rasterlogo2021.png",
                        "https://raster.repl.co/static/images/rasterlogo2021.png",
                        "https://raster.repl.co/static/images/rasterlogo2021.png",
                    ],
                )
            ],
            "Test Presentation",
            uuid.uuid4(),
            uuid.uuid4(),
        )
    else:
        pres = presentation.Presentation(
            [
                TextSlide(
                    "Hallo",
                    "when the impostor is sus " * 30,
                    "https://raster.repl.co/static/images/rasterlogo2021.png",
                ),
                TextSlide(
                    "Bawungus",
                    "got damn fr bruh no way bruh " * 30,
                    "https://raster.repl.co/static/images/rasterlogo2021.png",
                ),
                TextSlide(
                    ":skull:",
                    "when raster in a bikini is hot :flushed:" * 30,
                    "https://raster.repl.co/static/images/rasterlogo2021.png",
                ),
            ],
            "Test Presentation",
            uuid.uuid4(),
            uuid.uuid4(),
        )
    return jsonify(asdict(pres))

@viewer.route("/join_presentation", methods=["GET", "POST"])
def join_presentation():
    if request.method == "POST":
        try:
            room = database.get_room(request.form["room_code"])
        except RoomNotFoundException:
            pass
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
