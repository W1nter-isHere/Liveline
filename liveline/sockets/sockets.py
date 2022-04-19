from liveline.app import socket
from liveline.database import Room, database
from flask_socketio import join_room, leave_room, emit
from dataclasses import asdict

@socket.on("newRoom")
def new_room(pres):
    room = Room.create_and_add(pres["ID"])
    join_room(room.code)
    print(asdict(room))
    emit("newRoom", asdict(room))

@socket.on("pingRoom")
def ping_room(data):
    try:
        code = data['room']
        host_key = data['hostKey']
        if database.has_room(code):
            if database.get_room(code).host_key == host_key:
                database.ping_room(code)
    except KeyError:
        pass

@socket.on("join")
def on_join(data):
    room = data["room"]
    join_room(room)


@socket.on("changeSlide")
def change_slide(data):
    if "room" in data:
        room = data["room"]
        slide = data["slide"]
        emit("changeSlide", slide, to=room)

@socket.on("castVote")
def castVote(data):
    room = data["room"]
    slide = data["slide"]
    old_vote = data["oldVote"]
    new_vote = data["newVote"]
    
    emit("castVote", {
        "slide": slide,
        "oldVote": old_vote,
        "newVote": new_vote
    }, to=room)

@socket.on("save")
def save(data):
    index = data["index"]
    presentation_id = data["presentationID"]
    texts = data["texts"]
    images = data["images"]

    print(index)
    print(presentation_id)
    print(texts)
    print(images)

    if database.has_presentation(presentation_id):
        pres = database.get_presentation(presentation_id)
        slide = pres.slides[index]
        if len(texts) > 0:
            slide.title = texts[0]
        if slide.typ == "TextSlide":
            if len(texts) > 0:
                slide.text = texts[1]
        elif slide.typ == "TitleSlide":
            if len(images) > 0:
                slide.image = images[0]
        elif slide.typ == "ImageSlide":
            slide.images = images
        database.commit()

@socket.on("leave")
def on_leave(code):
    leave_room(code)


@socket.on("endPresentation")
def end_presentation(data):
    leave_room(data["room_code"])
    database.remove_room(data["room_code"])