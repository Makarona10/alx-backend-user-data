#!/usr/bin/env python3
'''Auth module'''

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Returns a salted hash of the input password"""
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def _generate_uuid() -> str:
    """Generates a uuid"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new a user"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pw = _hash_password(password)
            user = self._db.add_user(email, hashed_pw)
            return user
        raise ValueError(f"User {user} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Validates login process"""
        try:
            user = self._db.find_user_by(email=email)
            pw = password.encode('utf-8')
            return bcrypt.checkpw(pw, user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email) -> str:
        """creates a session for a user"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieves a user according to session id"""
        if session_id is not None:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                pass
        return None

    def destroy_session(self, user_id: int) -> None:
        """Gets rid of user session"""
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Resets password token"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token = str(uuid4())
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """updates user's password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pw = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_pw,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError
