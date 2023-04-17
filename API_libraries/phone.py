from typing import Optional, Any
from hippy.hip.device import HipDevice

# TODO: further endpoints methods to be implemenetd within ApiPhone class:
# GET phone/dtmf
# GET phone/calllog
# DELETE phone/calllog


class ApiPhone:
    '''
    This class is a wrapper around phone API.

    '''

    def __init__(self, device: HipDevice) -> None:
        '''
        Constract phone api
        :param device: Instance of HipDevice
        :return None
        '''
        self.device: HipDevice = device

    def get_status(self, account: Optional[int]) -> dict:
        '''requests info about sip accounts state
        :param account: request info only about particular account( e.g. 1, 2)
        :return: Dictionary representing result section of JSON response.
        '''
        return self._status(account)

    def _status(self, account: Optional[int], *, method: str = "GET") -> dict:
        params: dict[str, Any] = dict()
        if account:
            params['account'] = account

        return HipDevice.api_process_json_result(
            self.device.api_request(method, '/api/phone/status', params=params)
        )
