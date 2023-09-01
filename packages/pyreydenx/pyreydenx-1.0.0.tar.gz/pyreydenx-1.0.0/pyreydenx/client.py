import os
from typing import Optional, Dict

import requests

from .exceptions import InvalidCredentialsError, UnauthorizedError, NotFoundError, TooManyRequestsError, UnknownError
from .model.token import Token

BASE_URL = 'https://api.reyden-x.com/v1'


class Client:
    __slots__ = 'username', 'password', 'token',

    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        email = email or os.getenv('REYDENX_EMAIL')
        password = password or os.getenv('REYDENX_PASSWORD')

        if not email:
            raise ValueError('Email is required')

        if not password:
            raise ValueError('Password is required')

        self.username = email
        self.password = password
        self.token = None
        self.auth()

    @property
    def is_authenticated(self) -> bool:
        return self.token is not None and self.token.is_valid

    def auth(self):
        r = requests.post(f'{BASE_URL}/token/', data={
            'username': self.username,
            'password': self.password,
        }, headers={
            'Accept': 'application/json',
        }, timeout=5)
        if r.status_code == 200:
            self.token = Token(**r.json())
        else:
            self.token = None
            raise InvalidCredentialsError

    def request(self, method: str, path: str, payload: Optional[Dict] = None) -> Optional[Dict]:
        if not self.is_authenticated:
            raise UnauthorizedError

        headers = {
            'Authorization': f'Bearer {self.token.access_token}',
            'Accept': 'application/json'
        }
        path = f'{BASE_URL}{path}'
        if method == 'post':
            r = requests.post(path, json=payload, headers=headers, timeout=5)
        elif method == 'patch':
            r = requests.patch(path, headers=headers, timeout=5)
        else:
            r = requests.get(path, headers=headers, timeout=5)

        if r.status_code == 200:
            return r.json()
        elif r.status_code == 401:
            raise UnauthorizedError
        elif r.status_code == 404:
            raise NotFoundError
        elif r.status_code == 429:
            raise TooManyRequestsError
        raise UnknownError

    def get(self, path: str) -> Optional[Dict]:
        return self.request('get', path)

    def post(self, path: str, payload: Dict) -> Optional[Dict]:
        return self.request('post', path, payload)

    def patch(self, path: str) -> Optional[Dict]:
        return self.request('patch', path)
