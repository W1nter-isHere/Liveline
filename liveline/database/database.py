from __future__ import annotations

import flask_login

from typing import Dict, List, Any
from pathlib import Path
from dataclasses import asdict, dataclass
import json
import uuid
from random import randint

from liveline.logger import logger
from liveline.presentation.presentation import Presentation
import logging

USERS_PATH = Path("./database/database.json")
PFP_PATH = "/static/resources/users/"
PRESENTATION_PATH = "/static/resources/presentations/"

logger.setLevel(logging.DEBUG)
logger.info("Initiallizing database...")


class UserNotFoundException(Exception):
    pass

class PresentationNotFoundException(Exception):
    pass

class RoomNotFoundException(Exception):
    pass

class User(flask_login.UserMixin):
    username: str
    password: str
    pfp_path: str
    presentations: List[str]

    def __init__(self):
        super().__init__()
        self.id = str(uuid.uuid4())
        self.pfp_path = PFP_PATH + "unknown_user.svg"
        self.presentations = []

    # serialize user into a json object
    def serialize(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "password": self.password,
            "id": self.id,
            "pfp_path": self.pfp_path,
            "presentations": self.presentations,
        }

    # deserialize user back into a python object from a json object
    @staticmethod
    def deserialize(inp: Dict[str, Any]) -> User:
        user = User()
        user.username = inp["username"]
        user.password = inp["password"]
        user.id = inp["id"]
        user.pfp_path = inp["pfp_path"]
        user.presentations = inp["presentations"]
        return user

    def __repr__(self) -> str:
        return f"User(username={self.username}, id={self.id}, password={self.password}, pfp_path={self.pfp_path})"


@dataclass
class Room:
    code: str
    host_key: str
    presentation: str

    # deserialize user back into a python object from a json object
    @staticmethod
    def deserialize(inp: Dict[str, Any]) -> Room:
        room = Room(inp["code"], inp["host_key"], inp["presentation"])
        return room
    
    @staticmethod
    def create_unique(presentation: str) -> Room:
        return Room(
            Room.gen_unique_room_code(),
            Room.gen_host_key(),
            presentation
        )

    @staticmethod
    def create_and_add(presentation: str) -> Room:
        room = Room.create_unique(presentation)
        database.add_room(room)
        return room

    @staticmethod
    def gen_host_key():
        return uuid.uuid4().hex

    @staticmethod
    def gen_room_code():
        return "".join([str(randint(0, 9)) for _ in range(6)])
    
    @staticmethod
    def gen_unique_room_code():
        while database.has_room(code := Room.gen_room_code()):
            pass
        return code


class Database:
    __users: List[User]
    __presentations: List[Presentation]
    __rooms: List[Room]

    def __init__(self):
        self.reload_json()

    # load data from json
    def reload_json(self):
        if not USERS_PATH.exists():
            USERS_PATH.parent.mkdir(exist_ok=True)
            with open(USERS_PATH, "w") as f:
                json.dump({"users": [], "presentations": [], "rooms": []}, f)

        with open(USERS_PATH) as f:
            data: Dict[str, List[Any]] = json.load(f)
            self.deserialize(data)

    ###################################

    # check if user with username exist
    def has_user_with_username(self, username: str) -> bool:
        try:
            self.get_user_with_username(username)
        except UserNotFoundException:
            return False
        return True

    # get user with username
    # Exceptions: raises UserNotFoundException if not found
    def get_user_with_username(self, username: str) -> User:
        "Takes username, and returns user with that username."
        self.reload_json()
        for user in self.__users:
            if user.username == username:
                return user

        raise UserNotFoundException

    # check if user with id exist
    def has_user(self, id: str) -> bool:
        try:
            self.get_user(id)
        except UserNotFoundException:
            return False
        return True

    # get user with id
    # Exceptions: raises UserNotFoundException if not found
    def get_user(self, id: str) -> User:
        self.reload_json()
        for user in self.__users:
            if user.id == id:
                return user

        raise UserNotFoundException

    # add user to database
    # Side Effects: Causes Json Dump with new data
    def add_user(self, user: User):
        self.__users.append(user)
        self.commit()

    ##################################################

    # get room with id
    # raises the RoomNotFoundExpcetion if room with code is not found
    def get_room(self, code: str) -> Room:
        self.reload_json()
        for room in self.__rooms:
            if room.code == code:
                return room

        raise RoomNotFoundException

    # check if room with code exist
    def has_room(self, code: str) -> bool:
        try:
            self.get_room(code)
        except RoomNotFoundException:
            return False
        return True
    
    def add_room(self, room: Room):
        self.__rooms.append(room)
        self.commit()

    def remove_room(self, room_code):
        self.__rooms = list(filter(lambda room: room.code != room_code, self.__rooms))
        self.commit()

    ##################################################

    # get presentation with owner id
    def get_presentations_with_owner(self, owner_id: str) -> List[Presentation]:
        self.reload_json()
        return list(filter(lambda pres: pres.creator == owner_id, self.__presentations))

    # check if presentation with id exist
    def has_presentation(self, id: str) -> bool:
        try:
            self.get_presentation(id)
        except PresentationNotFoundException:
            return False
        return True

    # get presentation with id
    # Exceptions: raises PresentationNotFoundException if not found
    def get_presentation(self, id: str) -> Presentation:
        self.reload_json()
        for presentation in self.__presentations:
            if presentation.identifier == id:
                return presentation

        raise PresentationNotFoundException

    # add presentation to database
    # Side Effects: Causes Json Dump with new data
    def add_presentation(self, pres: Presentation):
        self.__presentations.append(pres)
        self.commit()

    ######################################

    # dump data into database json
    def commit(self):
        with open(USERS_PATH, "w") as f:
            json.dump(self.serialize(), f, indent=4)
        pass

    # serialize all database objects into json
    def serialize(self):
        return {
            "users": self.serialize_users(),
            "presentations": self.serialize_presentations(),
            "rooms": self.serialize_rooms(),
        }

    # deserializes all database objects from json
    def deserialize(self, data):
        try:
            self.__users = Database.deserialize_users(data["users"])
            self.__presentations = Database.deserialize_presentations(data["presentations"])
            self.__rooms = Database.deserialize_rooms(data["rooms"])
        except KeyError:
            pass

    # serialize users in database to json
    def serialize_users(self) -> List[Dict[str, str]]:
        return list(map(lambda user: user.serialize(), self.__users))

    # deserialize users in database from json
    @staticmethod
    def deserialize_users(users) -> List[User]:
        return list(map(lambda user: User.deserialize(user), users))

    def serialize_presentations(self) -> List[Dict[str, Any]]:
        return list(map(lambda pres: asdict(pres), self.__presentations))

    @staticmethod
    def deserialize_presentations(presentations) -> List[Presentation]:
        return list(
            map(lambda pres: Presentation.deserialize_presentation(pres), presentations)
        )

    def serialize_rooms(self) -> List[Dict[str, Any]]:
        return list(map(lambda room: asdict(room), self.__rooms))

    @staticmethod
    def deserialize_rooms(rooms) -> List[Room]:
        return list(map(lambda room: Room.deserialize(room), rooms))


database: Database = Database()
