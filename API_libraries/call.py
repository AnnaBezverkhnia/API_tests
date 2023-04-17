from hippy.hip.device import HipDevice
from typing import Optional, Any


class ApiCall:
    '''This class is wrapper around call API and provides methods for working with call sessions
    '''

    def __init__(self, device: HipDevice) -> None:
        '''Construct Call object
        :param device: Instance of HipDevice
        :return: None
        '''
        self.device: HipDevice = device

    def get_status(self, session: Optional[int] = None) -> dict:
        '''List and get info about call session status on the device
        :param session: particular call session id. None mandatory.
        If no session id is passed as a parameter, all existing call sessions info is retured in response.
        :return: Dictionary representing result section of JSON response.
        '''

        return self._status(session)

    def _status(self, session: Optional[int] = None, *, method: str = 'GET') -> dict:
        params = dict()
        if session is not None:
            params['session'] = session

        return HipDevice.api_process_json_result(
            self.device.api_request(method, '/api/call/status', params=params)
        )

    def post_dial(self, number: Optional[str] = None, users: Optional[list[str]] = None) -> dict:
        '''Initializes call session. Either number or user(s) parameter is mandatory
        :param number: calling destination number.
        :param users: List of user ids, separated with commas
        :return: Dictionary representing result section of JSON response. Contains unique call session id
        '''
        return self._dial(number, users)

    def _dial(self, number: Optional[str] = None, users: Optional[list[str]] = None, *, method: str = 'POST') -> dict:
        params: dict[str, Any] = dict()
        if number is not None:
            params['number'] = number

        if users is not None:
            users_str = ",".join(users)
            params['users'] = users_str
        return HipDevice.api_process_json_result(
            self.device.api_request(method, '/api/call/dial', params=params)
        )

    def post_answer(self, session: int) -> None:
        '''Answer incoming call
        :param session: particular call session id. Mandatory param
        :return: None
        '''

        self._answer(session)

    def _answer(self, session: int, *, method: str = 'POST') -> None:
        params = dict()
        if session is not None:
            params['session'] = session

        HipDevice.api_process_json_success(
            self.device.api_request(method, '/api/call/answer', params=params)
        )

    def post_hangup(self, session: int, reason: Optional[str] = None) -> None:
        '''Hangup incoming call
        :param session: particular call session id. Mandatory param.
        :reason: optional parameter. Values: normal,busy, rejected, noasnswer.
        :return: None
        '''
        self._hangup(session, reason)

    def _hangup(self, session: int, reason: Optional[str] = None, *, method: str = 'POST') -> None:
        params: dict[str, Any] = dict()
        if session is not None:
            params['session'] = session

        if reason is not None:
            params['reason'] = reason

        HipDevice.api_process_json_success(
            self.device.api_request(method, '/api/call/hangup', params=params)

        )
