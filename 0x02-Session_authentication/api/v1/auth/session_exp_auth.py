#!/usr/bin/env python3
""" SessionExpAuth module """

import os
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    '''SessionAuth class'''
    def __init__(self):
        '''SessionExpAuth initialization function'''
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
            if not self.session_duration:
                self.session_duration = 0
        except TypeError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        '''Creates a session id'''
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        SessionAuth.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        '''Returns user_id or None of no session_id'''
        s_dic = SessionAuth.user_id_by_session_id
        if not session_id or\
           session_id not in list(s_dic.keys()):
            return None
        if self.session_duration == 0:
            return s_dic.get(session_id).get("user_id")
        if not s_dic.get(session_id).get("created_at"):
            return None
        if s_dic.get(session_id).get("created_at")\
           + timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return s_dic.get(session_id).get("user_id")
