import pytest

from hippy.hip.device import *
from hippy.hip.api.dir import ApiDir
from hippy.hip.api.system import ApiSystem
from tests.http_api import HttpApiTest
from .dir_templates import templates
from .constants import *
from tests.test_vector import InvalidTestVectorGenerator
from hip_features import Feature
import copy
from tests.shared_func import xfail_mark

tvgen: InvalidTestVectorGenerator = pytest.tvgen     # type: ignore

# ----------------------------------------------------------------------------
#  Fixtures
# ----------------------------------------------------------------------------


@pytest.fixture(scope='class')
# returns instance of ApiDir class, which contains endpoints from api/dir section
def directory(dut: HipDevice) -> ApiDir:
    return ApiDir(dut)


@pytest.fixture(scope='class')
# creates user in device phonebook
def create_user(dut: HipDevice) -> dict:
    ApiDir(dut).put_create(users=CREATE_USER_FIXTURE)
    return ApiDir(dut).post_query()['users'][0]


@pytest.fixture(scope='class')
# creates user in device phonebook
def create_2_users(dut: HipDevice) -> list:
    ApiDir(dut).put_create(users=CREATE_2_USERS_FIXTURE)
    return ApiDir(dut).post_query()['users']


# ------------------
# --------------------------------------------------------
#  GET /api/dir/template
# --------------------------------------------------------------------------

@pytest.mark.hipfeature(Feature.DIRECTORY)
class TestDirTemplate(HttpApiTest):

    # ---  Generic API tests  ---

    service = HttpApiTest.Service.System
    privilege = HttpApiTest.Privilege.Control
    alt_valid_methods = ['POST']
    invalid_methods = ['DELETE', 'PUT']

    def command(self, dev: HipDevice, fixtures: dict, method: Optional[str] = None):
        ApiDir(dev)._template(method=method or 'GET')

    # ---  Parameter testing  ---

    def test_dir_template(self, directory, dut):
        model = ApiSystem(dut).get_info()['firmwarePackage']
        if model in ['accessunit2', 'accessunitm']:
            model = 'accessunit'
        rsp = directory.get_template()
        assert rsp['users'] == templates[model]

# --------------------------------------------------------------------------
#  GET /api/dir/get
# --------------------------------------------------------------------------

@pytest.mark.hipfeature(Feature.DIRECTORY)
class TestDirGet(HttpApiTest):

    # ---  Generic API tests  ---

    service = HttpApiTest.Service.System
    privilege = HttpApiTest.Privilege.Control
    invalid_methods = ['GET', 'DELETE', 'PUT']

    def command(self, dev: HipDevice, fixtures: dict, method: Optional[str] = None):
        if not method:
            ApiDir(dev).post_get()
        else:
            HipDevice.api_process_json_result(
                dev.api_request(method, '/api/dir/get')    # will result in an error -> don't care about params
            )

    # ---  Parameter testing  ---

    def test_get_user_valid_uuid(self, directory, create_user):
        # send request to api/dir/get with the parameter users and valid uuid
        # expected user data to be returned (user with specified uuid)
        uuid = create_user['uuid']
        rsp = directory.post_get(users=[{'uuid': uuid}])
        assert rsp['users'][0]['uuid'] == uuid

    @pytest.mark.parametrize('uuid', xfail_mark(tvgen.uuid(), '', "HIP-14184"))
    def test_get_user_invalid_uuid(self, directory, uuid):
        # send request to api/dir/get with the parameter users and invalid uuid
        # expected error (invalid uuid)
        rsp = directory.post_get(users=[{"uuid": uuid}])
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.UUID_INVALID.value

    def test_get_user_non_existing_uuid(self, directory):
        # send request with valid users parameter. Uuid has valid format, but does not exist in phonebook
        # expected error (uuid does not exist)
        rsp = directory.post_get(users=[{"uuid": UUID_VALID_FORMAT}])
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.UUID_DOES_NOT_EXIST.value

    def test_get_empty_fields(self, directory, create_user):
        # send request with empty list as a value of parameter fields and specified uuid.
        # all parameters of given user are expeced to be returned, including those with empty values
        uuid = create_user['uuid']
        user_param_number = len(create_user)
        rsp = directory.post_get(fields=[], users=[{'uuid': uuid}])
        assert len(rsp['users'][0]) > user_param_number

    def test_get_missing_fields(self, directory, create_user):
        # request existing user data (valid uuid is specified in request)
        # no fields param is included in request. Expect all fields containing non-default values to be returned.
        uuid = create_user['uuid']
        create_user_params = [param for param in create_user]
        rsp = directory.post_get(users=[{'uuid': uuid}])
        result_user_params = [param for param in rsp['users'][0]]
        assert result_user_params == create_user_params

    def test_get_valid_fields_param(self, directory, create_user):
        # request existing user data (valid uuid and valid fields are specified in the request)
        # expected only specified fields values to be returned
        uuid = create_user['uuid']
        rsp = directory.post_get(fields=[FieldParams.VALID_FIELDS.value[0]], users=[{'uuid': uuid}])
        result_user_params = [param for param in rsp['users'][0]]
        assert FieldParams.VALID_FIELDS.value[0] in result_user_params
        assert FieldParams.VALID_FIELDS.value[1] not in result_user_params

    def test_get_invalid_fields_param(self, directory, create_user):
        # request existing user data (valid uuid and invalid fields are specified in the request)
        # expected invalid parameter to be ignnored. Only uuid and timestamp should be received.
        uuid = create_user['uuid']
        rsp = directory.post_get(fields=[FieldParams.UNKNOWN_FIELD.value], users=[{'uuid': uuid}])
        result_user_params = [param for param in rsp['users'][0]]
        assert FieldParams.DEFAULT_VALUES.value[0] in result_user_params
        assert FieldParams.DEFAULT_VALUES.value[1] in result_user_params
        assert len(result_user_params) == 2


@pytest.mark.hipfeature(Feature.DIRECTORY)
class TestDirCreate(HttpApiTest):

    # ---  Generic API tests  ---

    service = HttpApiTest.Service.System
    privilege = HttpApiTest.Privilege.Control
    invalid_methods = ['DELETE', 'POST', 'GET']

    def command(self, dev: HipDevice, fixtures: dict, method: Optional[str] = None):
        if not method:
            ApiDir(dev).post_get()
        else:
            HipDevice.api_process_json_result(
                dev.api_request(method, '/api/dir/create')    # will result in an error -> don't care about params
            )

    # ---  Parameter testing  ---

    def test_create_valid_user_params(self, directory):
        # send request with users parameter valid value
        # expected a user to be created in dut phonebook
        CREATE_USER_TEST = copy.deepcopy(CREATE_USER_FIXTURE)
        rsp = directory.put_create(users=CREATE_USER_TEST)
        assert rsp['users'][0]['uuid'] == CREATE_USER_TEST[0]['uuid']


    @pytest.mark.parametrize('uuid', xfail_mark(tvgen.uuid(), '', 'HIP-14184'))
    def test_create_invalid_uuid(self, directory, uuid):
        CREATE_USER_TEST = copy.deepcopy(CREATE_USER_FIXTURE)
        # send request with users parameter, with invalid uuid value format
        # expected error EDIR_FIELD_VALUE_ERROR
        CREATE_USER_TEST[0]['uuid'] = uuid
        rsp = directory.put_create(users=CREATE_USER_TEST)
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.FIELD_VALUE_ERROR.value

    def test_create_uuid_already_exists(self, directory, create_user):
        # send request with users parameter, with the uuid already existing on device
        # expected error EDIR_UUID_ALREADY_EXISTS
        CREATE_USER_TEST = copy.deepcopy(CREATE_USER_FIXTURE)
        CREATE_USER_TEST[0]['uuid'] = create_user['uuid']
        rsp = directory.put_create(users=CREATE_USER_TEST)
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.USER_EXISTS.value

    def test_create_unknown_field(self, directory):
        # send request with users parameter, with invalid user parameter
        # expected error EDIR_FIELD_NAME_UNKNOWN
        CREATE_USER_TEST = copy.deepcopy(CREATE_USER_FIXTURE)
        CREATE_USER_TEST[0][FieldParams.UNKNOWN_FIELD.value] = FieldParams.UNKNOWN_FIELD.value
        rsp = directory.put_create(users=CREATE_USER_TEST)
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.UNKNOWN_FIELD.value

    def test_create_field_not_available(self, directory, dut):
        # send requet with user parameter, which is not available for particular device model
        # expected error message EDIR_FIELD_NOT_AVAILABLE
        CREATE_USER_TEST = copy.deepcopy(CREATE_USER_FIXTURE)
        model = ApiSystem(dut).get_info()['firmwarePackage']
        if model == 'style':
            CREATE_USER_TEST[0][FieldParams.FIELDS_NOT_AVAILABLE_STYLE.value] = FieldParams.FIELDS_NOT_AVAILABLE_STYLE.value
        else:
            CREATE_USER_TEST[0][FieldParams.FIELDS_NOT_AVAILABLE_ALL.value] = FieldParams.FIELDS_NOT_AVAILABLE_ALL.value
        rsp = directory.put_create(users=CREATE_USER_TEST)
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.FIELD_NOT_AVAILABLE.value

    def test_create_user_exists(self, directory, create_user):
        # send request with uuid, which already exists in device phonebook
        # expected error message EDIR_UUID_ALREADY_EXISTS
        rsp = directory.put_create(users=CREATE_USER_FIXTURE)
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.USER_ALREADY_EXISTS.value

    def test_create_force_overwrite_user(self, directory, create_user):
        # send request with uuid, which already exists in device phonebook. Set force on True
        # user will be overwritten using provided fields. Remaining fields will be set to default
        directory.put_create(force=True, users=OVERWRITE_EXISTING_USER)
        uuid = OVERWRITE_EXISTING_USER[0]['uuid']
        rsp = directory.post_get(users=[{'uuid': uuid}])
        result_user_params = [param for param in rsp['users'][0]]
        assert FieldParams.VALID_FIELDS.value[0] not in result_user_params
        assert rsp['users'][0]['name'] == OVERWRITE_EXISTING_USER[0]['name']


@pytest.mark.hipfeature(Feature.DIRECTORY)
class TestDirUpdate(HttpApiTest):

    # ---  Generic API tests  ---

    service = HttpApiTest.Service.System
    privilege = HttpApiTest.Privilege.Control
    invalid_methods = ['DELETE', 'POST', 'GET']

    def command(self, dev: HipDevice, fixtures: dict, method: Optional[str] = None):
        if not method:
            ApiDir(dev).post_get()
        else:
            HipDevice.api_process_json_result(
                dev.api_request(method, '/api/dir/create')    # will result in an error -> don't care about params
            )

    # ---  Parameter testing  ---

    def test_update_valid_user_params(self, directory, create_user):
        # send user update request, with valid user parameter update
        # expected the parameter to be updated accordin
        directory.put_update(UPDATE_EXISTING_USER)
        uuid = UPDATE_EXISTING_USER[0]['uuid']
        rsp = directory.post_get(users=[{'uuid': uuid}])
        assert rsp['users'][0]['access']['code'][0] == UPDATE_EXISTING_USER[0]['access']['code'][0]

    def test_update_non_existing_user(self, directory):
        # send user update request with uuid, which does not exist in device phone book
        # expected error message 'EDIR_UUID_DOES_NOT_EXIST'
        UPDATE_EXISTING_USER_COPY = copy.deepcopy(UPDATE_EXISTING_USER)
        UPDATE_EXISTING_USER_COPY[0]['uuid'] = UUID_VALID_FORMAT
        rsp = directory.put_update(UPDATE_EXISTING_USER_COPY)
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.UUID_DOES_NOT_EXIST.value

    def test_update_missing_uuid(self, directory):
        # send update request without uuid parameter
        # expected error message EDIR_UUID_IS_MISSING
        UPDATE_EXISTING_USER_COPY = copy.deepcopy(UPDATE_EXISTING_USER)
        UPDATE_EXISTING_USER_COPY[0].pop('uuid')
        rsp = directory.put_update(UPDATE_EXISTING_USER_COPY)
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.UUID_MISSING.value

    @pytest.mark.parametrize('uuid', xfail_mark(tvgen.uuid(), '', 'HIP-14184'))
    def test_update_invalid_uuid(self, directory, uuid):
        # send update request with invalid uuid parameter value
        # expected error message 'EDIR_UUID_INVALID_FORMAT
        UPDATE_EXISTING_USER_COPY = copy.deepcopy(UPDATE_EXISTING_USER)
        UPDATE_EXISTING_USER_COPY[0]['uuid'] = uuid
        rsp = directory.put_update(UPDATE_EXISTING_USER_COPY)
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.UUID_INVALID.value

    def test_update_unknown_field(self, directory, create_user):
        # send update request with unknown field parameter
        # expected error message EDIR_FIELD_NAME_UNKNOWN
        UPDATE_EXISTING_USER_COPY = copy.deepcopy(UPDATE_EXISTING_USER)
        UPDATE_EXISTING_USER_COPY[0][FieldParams.UNKNOWN_FIELD.value] = FieldParams.UNKNOWN_FIELD.value
        rsp = directory.put_update(UPDATE_EXISTING_USER_COPY)
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.UNKNOWN_FIELD.value

    def test_update_invalid_param_value(self, directory, create_user):
        # send update request with invalid parameter value
        # expected error message EDIR_FIELD_VALUE_ERROR
        rsp = directory.put_update(UPDATE_USER_INVALID_PARAM_VALUE)
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.FIELD_VALUE_ERROR.value


@pytest.mark.hipfeature(Feature.DIRECTORY)
class TestDirDelete(HttpApiTest):

    # ---  Generic API tests  ---

    service = HttpApiTest.Service.System
    privilege = HttpApiTest.Privilege.Control
    invalid_methods = ['DELETE', 'POST', 'GET']

    def command(self, dev: HipDevice, fixtures: dict, method: Optional[str] = None):
        if not method:
            ApiDir(dev).post_get()
        else:
            HipDevice.api_process_json_result(
                dev.api_request(method, '/api/dir/delete')    # will result in an error -> don't care about params
            )

    # ---  Parameter testing  ---

    def test_delete_existing_uuid(self, directory, create_user):
        # send request with parameter users and existing uuid
        # expected the user with specified uuid to be deleted
        uuid = create_user['uuid']
        directory.put_delete(users=[{'uuid': uuid}])
        rsp = directory.post_get(users=[{'uuid': uuid}])
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.UUID_DOES_NOT_EXIST.value

    @pytest.mark.parametrize('uuid', xfail_mark(tvgen.uuid(), '', 'HIP-14184'))
    def test_delete_invalid_uuid(self, directory, uuid):
        rsp = directory.put_delete(users=[{'uuid': uuid}])
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.UUID_INVALID.value

    @pytest.mark.xfail(reason='bug HIP-14215')
    def test_delete_without_params(self, directory):
        # send request without parameters
        # expected error
        with pytest.raises(HipDevice.RequestFailed) as e:
            directory.put_delete()
        assert e.value.error == HttpApiError.MISSING_PARAM
        assert e.value.description == ErrorMessages.ERROR_MISSING_PARAM.value

    @pytest.mark.xfail(reason='bug HIP-14216')
    def test_delete_invalid_owner_valid_uuid(self, directory, create_user):
        # send request with both valid uuid and invalid owner parameters
        # expected the user to be deleted
        uuid = create_user['uuid']
        directory.put_delete(DELETE_USER)
        rsp = directory.post_get(users=[{'uuid': uuid}])
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.UUID_DOES_NOT_EXIST.value

    def test_delete_existing_owner(self, directory, create_2_users):
        # create two users with same owner in dut phonebook. Send request with owner parameter
        # expected both users with the specified owner to be deleted
        owner = create_2_users[0]['owner']
        directory.put_delete(owner=owner)
        uuid1 = create_2_users[0]['uuid']
        uuid2 = create_2_users[1]['uuid']
        rsp = directory.post_get(users=[{'uuid': uuid1}, {'uuid': uuid2}])
        assert rsp['users'][0]['errors'][0]['code'] == ErrorMessages.UUID_DOES_NOT_EXIST.value
        assert rsp['users'][1]['errors'][0]['code'] == ErrorMessages.UUID_DOES_NOT_EXIST.value
