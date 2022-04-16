from __future__ import annotations

import flask_login

from typing import Dict, List, Any
from pathlib import Path
from dataclasses import asdict
import json
import uuid

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


class User(flask_login.UserMixin):
    username: str
    password: str
    pfp_path: str
    presentations: List[Presentation]

    def __init__(self):
        super().__init__()
        self.id = str(uuid.uuid4())
        self.pfp_path = PFP_PATH + "unknown_user.svg"
        self.presentations = []

    # serialize user into a json object
    def serialize(self) -> Dict[str, Any]:
        base = {
            "username": self.username,
            "password": self.password,
            "id": self.id,
            "pfp_path": self.pfp_path,
            "presentations": self.serialize_presentations()
        }

        return base
        # return self.__dict__

    def serialize_presentations(self):
        pres = []
        for presentation in self.presentations:
            if isinstance(presentation, dict):
                pres.append(presentation)
            else:
                pres.append(asdict(presentation))
        return pres

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


class Database:
    __users: List[User]

    def __init__(self):
        self.reload_json()

    # load data from json
    def reload_json(self):
        if not USERS_PATH.exists():
            USERS_PATH.parent.mkdir(exist_ok=True)
            with open(USERS_PATH, "w") as f:
                json.dump({"users": []}, f)

        with open(USERS_PATH) as f:
            data: Dict[str, List[Any]] = json.load(f)
            self.deserialize(data)

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

    # dump data into database json
    def commit(self):
        with open(USERS_PATH, "w") as f:
            json.dump(self.serialize(), f, indent=4)
        pass

    # serialize all database objects into json
    def serialize(self):
        return {"users": self.serialize_users()}

    # deserializes all database objects from json
    def deserialize(self, data):
        try:
            self.__users = Database.deserialize_users(data["users"])
        except KeyError:
            pass

    # serialize users in database to json
    def serialize_users(self) -> List[Dict[str, str]]:
        return list(map(lambda user: user.serialize(), self.__users))

    # deserialize users in database from json
    @staticmethod
    def deserialize_users(users) -> List[User]:
        return list(map(lambda user: User.deserialize(user), users))


database: Database = Database()
