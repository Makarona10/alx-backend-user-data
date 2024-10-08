#!/usr/bin/env python3
""" SessionAuth module """

from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    '''Session Auth class'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a Session ID for a user_id'''
        if user_id is None or type(user_id) is not str:
            return None
        sessionId = uuid4()
        SessionAuth.user_id_by_session_id[str(sessionId)] = user_id
        return str(sessionId)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''returns a User ID based on a Session ID'''
        if session_id is None or type(session_id) is not str:
            return None
        return str(SessionAuth.user_id_by_session_id.get(session_id))

    def current_user(self, request=None):
        '''returns a User instance based on a cookie value'''

        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(str(session_cookie))
        return User.get(user_id)

    def destroy_session(self, request=None):
        '''deletes the user session / logout'''
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        if not self.user_id_for_session_id(session_id):
            return False
        del self.user_id_by_session_id[session_id]
        return True
