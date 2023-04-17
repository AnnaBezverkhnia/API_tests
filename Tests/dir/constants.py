from dataclasses import dataclass
from typing import Optional
from enum import Enum


@dataclass
class CreateUser:
    owner: Optional[str] = None
    uuid: Optional[str] = None
    name:  Optional[str] = None
    callPos: Optional[list] = None
    access: Optional[dict] = None

    def as_dict(self):
        '''
        Function allows to create class instance only with parameters,
        which values are not None.
        '''
        result = self.__dict__
        return {key: value for key, value in result.items() if value is not None}


CREATE_USER_FIXTURE: list = [
        CreateUser(
            uuid="4c957905-5d3f-479b-839a-c7d5b2ae2db5",
            name="user1",
            callPos=[{"peer": "1234"}],
            access={"code": [
                        "666"
            ]},).as_dict(),
    ]

CREATE_2_USERS_FIXTURE: list = [
        CreateUser(
            owner="ACOM",
            uuid="4c957905-5d3f-479b-839a-c7d5b2ae2db5",
            name="user1",
            callPos=[{"peer": "1234"}],
            access={"code": [
                "666"
            ]},).as_dict(),
        CreateUser(
            owner="ACOM",
            uuid="4c957905-5d3f-479b-839a-c7d5b2ae2db6",
            name="user2",
            callPos=[{"peer": "1234"}],
            access={"code": [
                "666"
             ]},).as_dict(),
    ]

OVERWRITE_EXISTING_USER: list = [
        CreateUser(
            uuid="4c957905-5d3f-479b-839a-c7d5b2ae2db5",
            name="user1",
        ).as_dict(),
]

CREATE_USER: list = [
        CreateUser(
            uuid="4c957905-5d3f-479b-839a-c7d5b2ae2db5",
            name="user1",
            callPos=[{"peer": "1234"}],
        ).as_dict(),
]

UPDATE_EXISTING_USER: list = [
        CreateUser(
            uuid="4c957905-5d3f-479b-839a-c7d5b2ae2db5",
            name="user1",
            callPos=[{"peer": "1234"}],
            access={"code": [
                "999"
            ]},
        ).as_dict(),
]

UPDATE_USER_INVALID_PARAM_VALUE: list = [
        CreateUser(
            uuid="4c957905-5d3f-479b-839a-c7d5b2ae2db5",
            name="user1",
            access={"code": [
                "test"
            ]},
        ).as_dict(),
]

DELETE_USER: list = [
        CreateUser(
            owner="ACOM",
            uuid="4c957905-5d3f-479b-839a-c7d5b2ae2db5",
            name="user1",
            access={"code": [
                "test"
            ]},
        ).as_dict(),

]


class ErrorMessages(Enum):
    FUNC_NOT_SUPPORTED = 'function is not supported'
    UUID_DOES_NOT_EXIST = 'EDIR_UUID_DOES_NOT_EXIST'
    UUID_INVALID = 'EDIR_UUID_INVALID_FORMAT'
    FIELD_VALUE_ERROR = 'EDIR_FIELD_VALUE_ERROR'
    USER_EXISTS = 'EDIR_UUID_ALREADY_EXISTS'
    UNKNOWN_FIELD = 'EDIR_FIELD_NAME_UNKNOWN'
    FIELD_NOT_AVAILABLE = 'EDIR_FIELD_NOT_AVAILABLE'
    USER_ALREADY_EXISTS = 'EDIR_UUID_ALREADY_EXISTS'
    UUID_MISSING = 'EDIR_UUID_IS_MISSING'
    ERROR_MISSING_PARAM = 'missing mandatory parameter'


class FieldParams(Enum):
    UNKNOWN_FIELD = 'test'
    DEFAULT_VALUES = ['uuid', 'timestamp']
    VALID_FIELDS = ['access', 'name']
    FIELDS_NOT_AVAILABLE_ALL = 'recordType'
    FIELDS_NOT_AVAILABLE_STYLE = 'buttons'
    INVALID_VALUE = 'test'


UUID_VALID_FORMAT = '4c957905-5d3f-479b-839a-c7d5b2ae2333'
