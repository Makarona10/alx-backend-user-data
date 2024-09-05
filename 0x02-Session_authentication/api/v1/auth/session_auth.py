#!/usr/bin/env python3
""" SessionAuth module """

from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    '''Session Auth class'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a Session ID for a user_id'''
        if user_id is None:
            return None
        if type(user_id) is not str:
            None
        sessionId = uuid4()
        SessionAuth.user_id_by_session_id[sessionId] = user_id
        return sessionId
