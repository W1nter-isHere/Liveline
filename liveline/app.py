from flask import Flask, redirect, url_for, render_template
from os import getenv

import flask_login
from flask_socketio import SocketIO
from flask_apscheduler import APScheduler
import logging
import colorama

colorama.init()
from .logger import logger

logger.setLevel(logging.DEBUG)

from .blueprints import auth, profile, viewer, host

logger.info("Starting...")

app = Flask(__name__)
app.config.update(SECRET_KEY=getenv("SECRET_KEY"))

socket = SocketIO(app)
import liveline.sockets

scheduler = APScheduler()
# scheduler.api_enabled = True

import liveline.jobs

scheduler.init_app(app)
scheduler.start()

auth.init_login_manager(app)

logger.info('Loading "Auth" blueprint...')
app.register_blueprint(auth.auth, url_prefix="/auth")

logger.info('Loading "Profile" blueprint...')
app.register_blueprint(profile.profile, url_prefix="/profile")

logger.info('Loading "Viewer" blueprint...')
app.register_blueprint(viewer.viewer, url_prefix="/viewer")

logger.info('Loading "Host" blueprint...')
app.register_blueprint(host.host, url_prefix="/host")

@app.route("/")
def home():
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("profile.profile_page"))
    return render_template("home.html")


@app.errorhandler(404)
def handle_error(err):
    return redirect("/")


logger.info("Started.")
