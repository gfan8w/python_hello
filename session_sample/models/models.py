import datetime
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
    passphrase: Optional[str]




class DbSession(Model):
    session_key: str
    session_name: str
    token: str
    expiry_date: datetime.datetime


class ProfileReq(Model):
    firstname: str
    lastname:str
    middlename:str
    date_signed: datetime.date
    age: int
    date_signed: datetime.date
    occupation: str
    birthday: datetime.date
    address: str