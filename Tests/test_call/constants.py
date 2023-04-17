import string
from random import choice

CHARACTERS = string.printable

ERROR_MISSING_PARAM = f"missing mandatory parameter"
ERROR_INVALID_PARAM = f"invalid parameter value"
ERROR_PROCESSING = f"session not found"
ERROR_INVALID_USER = f"invalid UUID"

period = 3
timeout = 30

PARAMS_VALID_NUMBERS = [
    "10.27.36.6",
    "1234",
    "10.27.58.82",

]

PARAMS_INVALID_USERS = [
    "adgf-15adad-87dsada-adada",
    123654,
    "%%ˇ0%9989808797",
]

# minimum value for session id parameter −2,147,483,648 , maximum 2,147,483,647

# when invalid session id value param is sent, error 12 should be received.
PARAMS_INVALID_SESSION = [
    1233354545465465465,
    "4abcd",
    -2147483649,
    2147483648,
    True,
]

# when valid session id value param is sent, error 14 should be received.
PARAMS_SESSION_NOT_FOUND = [
    123456,
    1234564,
    -2147483648,
    -2147483647,
    2147483646,
    2147483647,
]

PARAMS_VALID_REASON = [
    'normal',
    'busy',
    'rejected',
    'noanswer',
]

PARAMS_INVALID_REASON = [
    'notnormal',
    'free',
    'accepted',
    123456,
    '+++++',
]
