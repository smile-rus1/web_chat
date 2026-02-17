from dataclasses import dataclass

from src.exceptions.base import BaseExceptions


class AuthException(BaseExceptions):
    ...


@dataclass
class InvalidUsername(AuthException):
    username: str

    def message(self):
        return f"User with this username {self.username} not registered"


class RefreshTokenNotValid(AuthException):
    def message(self):
        return f"Refresh token is not valid"
