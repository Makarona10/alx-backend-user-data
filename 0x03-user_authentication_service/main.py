#!/usr/bin/env python3
"""Program Main module"""

import requests


url = "http://127.0.0.1:5000"

def register_user(email: str, password: str) -> None:
    expected = {"email": email, "message": "user created"}
    res = requests.post(f'{url}/users', data={
        "email": email,
        "password": password,
    })
    assert res.status_code == 200
    assert res.json() == expected


if __name__ == "__main__":
    register_user("ahmed@maka.com", "newpassword")
