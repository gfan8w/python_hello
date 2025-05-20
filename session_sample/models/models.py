from bson import datetime
from typing import Optional

from odmantic import EmbeddedModel, Model


class Profile(EmbeddedModel):
    firstname: str
    lastname: str
    middlename: str
    date_signed: datetime.datetime
    age: int
    occupation: str
    birthday: datetime.datetime
    address: str


class Login(Model):
    __collection__ = "login"

    login_id: int
    username: str
    password: str
    passphrase: Optional[str] = None
    profile: list[Profile] = None # TypeError: string indices must be integers, not 'str', SO Make it a list to avoid the error





class DbSession(Model):
    session_key: str
    session_name: str
    token: str
    expiry_date: datetime.datetime
