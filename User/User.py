from .UserData import UserData
from GPSystem.GPRater import GPRater


class User:
    def __init__(self, username: str, is_guest: bool):
        self._username = username
        self._user_data = UserData()
        self._is_guest = is_guest
        self._gp = 0

    @property
    def username(self) -> str:
        return self._username

    @property
    def user_data(self) -> UserData:
        return self._user_data

    @property
    def gp(self) -> int:
        return self._gp

    def replace_data(self, json_str):
        self._user_data = UserData(json_str)

    def __repr__(self):
        print(self._username, self._gp, "GP")
        return ""
