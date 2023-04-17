import pytest
from typing import Optional
from random import choice, randrange
import operator

from hippy.hip.types import *
from hippy.hip.device import *
from hippy.hip.api.call import ApiCall
from hippy.hip.api.dir import ApiDir
from hippy.hip.api.phone import ApiPhone
from hip_features import Feature

from tests.http_api import HttpApiTest
from .constants import *
from tests.shared_func import *

'''wait_for function is being used in tests to ensure that there is no active
call session when another session is being initialized, for eliminating errors'''

# ----------------------------------------------------------------------------
#  Fixtures
# ----------------------------------------------------------------------------


# returns instance of Apicall class, which contains endpoints from Call section(status, dial, answer, hangup)
@pytest.fixture(scope='class')
def call(dut: HipDevice) -> ApiCall:
    return ApiCall(dut)


# returns user_id of the first user from dut directory
@pytest.fixture(scope="class")
def user_id(dut: HipDevice) -> dict:
    directory_query = ApiDir(dut).post_query(fields=["uuid"])
    return directory_query['users'][0]['uuid']


# send request to api/phone/status to check if sip1 account is enabled on dut
def phone_status(dut: HipDevice) -> dict:
    phone_status = ApiPhone(dut).get_status(account=1)
    return phone_status['accounts'][0]['enabled']


# creates HipDevice instance for another device, which will be used together with dut in some tests.
# e.g. for initializing incoming call to dut
# Ip address for additional_device is passed in pytestArgs
@pytest.fixture(scope='class')
def additional_device(request: pytest.FixtureRequest):
    '''Access to the additional device'''
    device = HipDevice(request.config.option.ADDITIONAL_DEVICE, ssl=False)
    with open('data/config/api-call-config.xml', 'rb') as file:
        device.upload_config(file.read())
    # Wait for the device to reload configuration
    time.sleep(HipDevice.DB_RELOAD_TIME)
    return ApiCall(device)

# --------------------------------------------------------------------------
#  GET /api/call/status
# --------------------------------------------------------------------------


@pytest.mark.hipconfig('data/config/api-call-config.xml')
@pytest.mark.hipfeature(Feature.PHONE)
class TestCallStatus(HttpApiTest):

    # ---  Generic API tests  ---

    service = HttpApiTest.Service.Call
    privilege = HttpApiTest.Privilege.Monitor
    alt_valid_methods = ['POST']
    invalid_methods = ['DELETE', 'PUT']

    def command(self, dev: HipDevice, fixtures: dict, method: Optional[str] = None):
        ApiCall(dev)._status(method=method or 'GET')

    # ---  Parameter testing  ---

    # send request without parameters
    def test_call_status(self, dut, call):
        rsp = call.get_status()
        assert type(rsp['sessions']) == list
        assert 'sessions' in rsp

    # send request with valid session id
    def test_call_status_valid_session(self, dut, call, user_id):
        wait_for({'sessions': []}, timeout, period, target_func=ApiCall(dut).get_status)
        # initialize the call with the user from directory and get session id
        rsp = call.post_dial(users=user_id)
        session_id = rsp['session']
        rsp = call.get_status(session=session_id)  # send request with existing session parameter
        assert len(rsp['sessions']) == 1
        assert rsp['sessions'][0]['session'] == session_id

    # send request with invalid session id param value
    @pytest.mark.parametrize('session_id', PARAMS_INVALID_SESSION)
    def test_call_status_invalid_session(self, dut, call, session_id):
        wait_for({'sessions': []}, timeout, period, target_func=call.get_status)
        with pytest.raises(HipDevice.RequestFailed) as e:
            call.get_status(session=session_id)
        assert e.value.error == HttpApiError.INVALID_PARAM
        assert e.value.description == ERROR_INVALID_PARAM

    # send request with valid session id param value, but non-existing session id
    @pytest.mark.parametrize('session_id', PARAMS_SESSION_NOT_FOUND)
    def test_call_status_session_not_found(self, dut, call, session_id):
        wait_for({'sessions': []}, 30, 3, target_func=ApiCall(dut).get_status)
        with pytest.raises(HipDevice.RequestFailed) as e:
            call.get_status(session=session_id)  # send request with non-existing session id
        assert e.value.error == HttpApiError.PROCESSING
        assert e.value.description == ERROR_PROCESSING

# --------------------------------------------------------------------------
#  GET /api/call/dial
# --------------------------------------------------------------------------


@pytest.mark.hipconfig('data/config/api-call-config.xml')
@pytest.mark.hipfeature(Feature.PHONE)
class TestDial(HttpApiTest):

    # ---  Generic API tests  ---

    service = HttpApiTest.Service.Call
    privilege = HttpApiTest.Privilege.Control
    alt_valid_methods = ['POST']
    invalid_methods = ['DELETE', 'PUT']

    def command(self, dev: HipDevice, fixtures: dict, method: Optional[str] = None):
        wait_for({'sessions': []}, timeout, period, target_func=ApiCall(dev)._status)
        ApiCall(dev)._dial(number=PARAMS_VALID_NUMBERS[1], method=method or 'GET')

    # ---  Parameter testing  ---

    # send request without mandatory parameters
    def test_dial_call(self, dut, call):
        wait_for({'sessions': []}, 30, 3, target_func=ApiCall(dut).get_status)  # wait for no session to be in progress
        with pytest.raises(HipDevice.RequestFailed) as e:
            call.post_dial()
        # Test if given error code and description is correct
        assert e.value.error == HttpApiError.MISSING_PARAM
        assert e.value.description == ERROR_MISSING_PARAM

    # send request with only one mandatory parameter: 'number'
    @pytest.mark.parametrize('number', PARAMS_VALID_NUMBERS)
    def test_dial_valid_number(self, dut, number, call):
        wait_for(True, timeout, period, target_func=lambda: phone_status(dut))
        wait_for({'sessions': []}, timeout, period, target_func=call.get_status)  # wait for no session to be in progress
        # Initialize the call. Session id is a number, other that 0
        rsp = call.post_dial(number=f'sip:{number}')
        session_id = rsp['session']
        assert session_id != 0

    # send request with only one valid mandatory parameter: 'user'.
    def test_dial_valid_user(self, dut, user_id, call):
        wait_for({'sessions': []}, 30, 3, target_func=call.get_status)
        # Initialize the call. Session id is a number, other than 0
        rsp = call.post_dial(users=user_id)
        session_id = rsp['session']
        assert session_id != 0

    # send request with with invalid user param
    @pytest.mark.parametrize('users', PARAMS_INVALID_USERS)
    def test_dial_invalid_user(self, dut, users, call):
        wait_for({'sessions': []}, timeout, period, target_func=call.get_status)
        with pytest.raises(HipDevice.RequestFailed) as e:
            call.post_dial(users=users)
        assert e.value.error == HttpApiError.INVALID_PARAM
        assert e.value.description == ERROR_INVALID_USER

# --------------------------------------------------------------------------
#  GET /api/call/answer
# --------------------------------------------------------------------------


@pytest.mark.hipconfig('data/config/api-call-config.xml')
@pytest.mark.hipfeature(Feature.PHONE)
class TestAnswerCall(HttpApiTest):

    # ---  Generic API tests  ---

    service = HttpApiTest.Service.Call
    privilege = HttpApiTest.Privilege.Control
    alt_valid_methods = ['POST']
    invalid_methods = ['DELETE', 'PUT']

    def command(self, dev: HipDevice, fixtures: dict[str, Any], method: Optional[str] = None):
        wait_for({'sessions': []}, timeout, period, target_func=ApiCall(dev).get_status)
        try:
            ApiCall(dev)._answer(session= PARAMS_SESSION_NOT_FOUND[0], method=method or 'GET')
        except HipDevice.RequestFailed as e:
            if e.error == HttpApiError.PROCESSING:  # ignore "session not found" error
                pass
            else:
                raise e

    # ---  Parameter testing  ---

    # send request without mandatory parameters
    def test_answer_no_param(self, call, dut):
        wait_for({'sessions': []}, timeout, period, target_func=call.get_status)
        with pytest.raises(HipDevice.RequestFailed) as e:
            call.post_answer(session=None)
        assert e.value.error == HttpApiError.MISSING_PARAM
        assert e.value.description ==ERROR_MISSING_PARAM

    # send request with valid call session
    def test_answer_valid_session(self, additional_device, call, dut):
        # use another HipDevice to initialize incoming call to dut
        wait_for({'sessions': []}, 30, 3, target_func=additional_device.get_status)
        additional_device.post_dial(number=f'sip:{dut._address}')
        sesiion_list = wait_for(1, timeout, period, lambda: call.get_status()['sessions'], operator_func=compare_result_len)
        session_id = sesiion_list[0]['session']
        rsp = call.post_answer(session=session_id)
        assert rsp is None

    # send request with invalid call session id parameter value
    @pytest.mark.parametrize('session', PARAMS_INVALID_SESSION)
    def test_answer_invalid_session(self, call, session, dut):
        wait_for({'sessions': []}, 30, 3, target_func=call.get_status)
        with pytest.raises(HipDevice.RequestFailed) as e:
            call.post_answer(session=session)
        assert e.value.error == HttpApiError.INVALID_PARAM
        assert e.value.description == ERROR_INVALID_PARAM

    # send request with invalid session id, but valid parameter value
    @pytest.mark.parametrize('session', PARAMS_SESSION_NOT_FOUND)
    def test_answer_session_not_found(self, call, session, dut):
        wait_for({'sessions': []}, timeout, period, target_func=call.get_status)
        with pytest.raises(HipDevice.RequestFailed) as e:
            call.post_answer(session=session)
        assert e.value.error == HttpApiError.PROCESSING
        assert e.value.description == ERROR_PROCESSING

# --------------------------------------------------------------------------
#  GET /api/call/hangup
# --------------------------------------------------------------------------


@pytest.mark.hipconfig('data/config/api-call-config.xml')
@pytest.mark.hipfeature(Feature.PHONE)
class TestCallHangup(HttpApiTest):

    # ---  Generic API tests  ---

    service = HttpApiTest.Service.Call
    privilege = HttpApiTest.Privilege.Control
    alt_valid_methods = ['POST']
    invalid_methods = ['DELETE', 'PUT']

    def command(self, dev: HipDevice, fixtures: dict, method: Optional[str] = None):
        wait_for({'sessions': []}, timeout, period, target_func=ApiCall(dev).get_status)
        try:
            ApiCall(dev)._hangup(session= PARAMS_SESSION_NOT_FOUND[0], method=method or 'GET')
        except HipDevice.RequestFailed as e:
            if e.error == HttpApiError.PROCESSING:  # ignore "session not found" error
                pass
            else:
                raise e

    # ---  Parameter testing  ---

    # send request with valid call session id
    def test_hangup_valid_session_no_reason(self, additional_device, call, dut):
        # use another HipDevice to initialize the call to dut
        wait_for({'sessions': []}, timeout, period, target_func=additional_device.get_status)
        additional_device.post_dial(number=f'sip:{dut._address}')
        session_list = wait_for(1, timeout, period, lambda: call.get_status()['sessions'], operator_func=compare_result_len)
        session_id = session_list[0]['session']
        rsp = call.post_hangup(session=session_id)
        assert rsp is None

    # send request with valid session idand valid reason parameteres
    @pytest.mark.parametrize('reason', PARAMS_VALID_REASON)
    def test_hangup_valid_session_reason(self, additional_device, call, dut, reason):
        # use another HipDevice to initialize the call to dut
        wait_for({'sessions': []}, timeout, period, target_func=additional_device.get_status)
        additional_device.post_dial(number=f'sip:{dut._address}')
        session_list = wait_for(1, timeout, period, lambda: call.get_status()['sessions'], operator_func=compare_result_len)
        session_id = session_list[0]['session']
        rsp = call.post_hangup(session=session_id)
        assert rsp is None

    # send request with invalid reason parameter
    @pytest.mark.parametrize('reason', PARAMS_INVALID_REASON)
    def test_hangup_valid_session_invalid_reason(self, additional_device, call, dut, reason):
        # create another HipDevice to initialize the call to dut
        wait_for({'sessions': []}, timeout, period, target_func=additional_device.get_status)
        additional_device.post_dial(number=f'sip:{dut._address}')
        # wait untill dut creates incoming call session on its side
        session_list = wait_for(1, timeout, period, lambda: call.get_status()['sessions'], operator_func=compare_result_len)
        session_id = session_list[0]['session']
        with pytest.raises(HipDevice.RequestFailed) as e:
            call.post_hangup(session=session_id, reason=reason)
        assert e.value.error == HttpApiError.INVALID_PARAM
        assert e.value.description == ERROR_INVALID_PARAM

    # send request with empty session parameter
    def test_hangup_without_session_param(self, call, dut):
        wait_for({'sessions': []}, timeout, period, target_func=call.get_status)
        with pytest.raises(HipDevice.RequestFailed) as e:
            call.post_hangup(session=None)
        assert e.value.error == HttpApiError.MISSING_PARAM
        assert e.value.description == ERROR_MISSING_PARAM

    # send request with invalid call session id parameter value. Without reason parameter
    @pytest.mark.parametrize('session', PARAMS_INVALID_SESSION)
    def test_hangup_invalid_session(self, call, session, dut):
        wait_for({'sessions': []}, timeout, period, target_func=call.get_status)
        with pytest.raises(HipDevice.RequestFailed) as e:
            call.post_hangup(session=session)
        assert e.value.error == HttpApiError.INVALID_PARAM
        assert e.value.description == ERROR_INVALID_PARAM

    # send request with non-existing session id, but valid session id parameter value. Without reason parameter
    @pytest.mark.parametrize('session', PARAMS_SESSION_NOT_FOUND)
    def test_hangup_session_not_found(self, call, session, dut):
        wait_for({'sessions': []}, timeout, period, target_func=call.get_status)
        with pytest.raises(HipDevice.RequestFailed) as e:
            call.post_hangup(session=session)
        assert e.value.error == HttpApiError.PROCESSING
        assert e.value.description == ERROR_PROCESSING

