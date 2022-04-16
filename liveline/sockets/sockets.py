from liveline.app import app, socket
from liveline.database import Room, database
from flask_socketio import join_room, leave_room, send, emit
import uuid
from dataclasses import asdict

@socket.on("newRoom")
def new_room(pres):
    room = Room.create_and_add(pres)
    print("created room with code: " + room.code)
    join_room(room.code)
    emit("newRoom", asdict(room))


@socket.on("join")
def on_join(data):
    room = data["room"]
    join_room(room)


@socket.on("changeSlide")
def change_slide(data):
    room = data["room"]
    slide = data["slide"]
    print(data)
    emit("changeSlide", slide, to=room)


@socket.on("leave")
def on_leave(code):
    leave_room(code)


@socket.on("endPresentation")
def end_presentation(room_code):
    leave_room(room_code)
    database.remove_room(room_code)