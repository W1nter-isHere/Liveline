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

room = Blueprint(
    "room", __name__, static_folder="static", template_folder="templates"
)

@room.route("/<code>")
def view_room(code):
