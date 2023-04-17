from typing import Optional, Any
from hippy.hip.device import HipDevice
from hippy.hip.types import BlobType, BlobParam
import json


class ApiDir:
    '''
    This class is wrapper around directory API.

    '''

    def __init__(self, device: HipDevice) -> None:
        '''
        Construct directory object

        :param device: Instance of HipDevice
        :return: None
        '''
        self.device: HipDevice = device

    def get_template(self) -> dict:
        '''
        A template response contains all directory attributes of current device
        '''
        return self._template()

    def _template(self, *, method: str = 'GET') -> dict:

        return HipDevice.api_process_json_result(
            self.device.api_request(method, '/api/dir/template')
        )

    def post_get(self, fields: Optional[list[str]] = None, users: Optional[list[Any]] = None) -> dict:
        '''
        function is used for retrieving fields of given list of users.
        Users are identified by UUIDs.

        :param fields: An optional array of field names to be returned. Field names
        are defined in the /api/dir/template function, uuid and timestamp fields
        are always returned and do not need to be specified. Groups of fields can be
        requested using a group (parent) name as shown in the table below.
        Two special cases of the fields parameter value are handled:

             - empty array - all available fields are returned
             - missing parameter - all fields containing non-default values are returned

        :param users: Optional array of users to get field values of. Id no usera are specified,
        an empty list is being returned.
        :return: Dictionary representing result section of JSON response.

        '''

        data: dict[str, Any] = {}
        if fields is not None:
            data["fields"] = fields
        if users is not None:
            data["users"] = users
        blob = BlobParam(BlobType.JSON, json.dumps(data).encode('utf-8'))
        return HipDevice.api_process_json_result(
            self.device.api_post('/api/dir/get', blob=blob)
        )

    def put_create(self, force: Optional[bool] = None, users: Optional[list[Any]] = None) -> dict:
        ''' function allows creating a list of users and setting selected fields.

        :param force: An optional boolean flag to force user creation (default value is false).
        If user with given UUID already exists and force flag is set to true, the existing
        user is overwritten using provided fields. Remaining fields are reset to default values.
        In case that the force flag is set to false or is not specified, the error code
        EDIR_UUID_ALREADY_EXISTS is returned.

        :param users: An optional array of users to be created. This array contains objects with
        specified fields and values. Available fields depend on the model type and can be obtained
        using the /api/dir/template function.
        :return: Dictionary representing result section of JSON response.

        '''

        data: dict[str, Any] = {}
        if force is not None:
            data["force"] = force
        if users is not None:
            data["users"] = users
        files = {BlobType.DIR_NEW.value: json.dumps(data).encode('utf-8')}

        return HipDevice.api_process_json_result(
            self.device.api_put('/api/dir/create', files=files)
        )

    def put_delete(self, owner: Optional[str] = None, users: Optional[list[Any]] = None) -> dict:
        '''function allows deleting a list of users given by their UUIDs (uuid is mandatory and
        the only expected field; another fields are ignored when provided).

        :param owner: A mandatory (if user is omitted) string to delete all users with specified owner.
        If owner parameter is omitted than the users parameter is expected.

        :param users: A mandatory (if owner is omitted) dictionary of users to be deleted.
        The json contains uuid keys with specified value.
        :return: Dictionary representing result section of JSON response.
        '''

        data: dict[str, Any] = {}
        if owner is not None:
            data["owner"] = owner
        if users:
            data["users"] = users
        files = {BlobType.DIR_NEW.value: json.dumps(data).encode('utf-8')}

        return HipDevice.api_process_json_result(
            self.device.api_put('/api/dir/delete', files=files)
        )

    def put_update(self, users: list[Any]) -> dict:
        '''function allows updating a list of users using provided fields. Users are identified by UUIDs
        (the UUID is mandatory field). Deleted field is ignored when provided. If a field does not exist
        or provided value is not accepted, an error is reported to the caller and the user is not updated.

        :param users: An array of users to be updated. This array contains objects with specified fields
        and values. Available fields depend on the model type and can be obtained using the
        /api/dir/template function. uuid field is mandatory.
        :return: Dictionary representing result section of JSON response.
        '''

        data: dict[str, Any] = {"users": users}
        files = {BlobType.DIR_NEW.value: json.dumps(data).encode('utf-8')}

        return HipDevice.api_process_json_result(
            self.device.api_put('/api/dir/update', files=files)
        )

    def post_query(self, fields: Optional[list[str]] = None, series: Optional[str] = None,
                   iterator: Optional[int] = 0) -> dict:
        '''function is used for retrieving fields of list of users in directory

        :param fields: An optional array of field names to be returned. Field names are defined in
        the /api/dir/template function, uuid and timestamp fields are always returned and do not
        need to be specified. Two special cases of the fields parameter value are handled:

            - empty array - all available fields are returned
            - missing parameter - all fields containing non-default values are returned

        :param series: An optional string parameter specifying expected directory series. This value is
        generated on a device factory reset and can be used by callers to validate if a device directory
        is in an expected state.

        :param iterator: The timestamp iterator has an integer parameter timestamp indicating first directory
        entry to be returned (last timestamp is returned by any of create, update or delete function).
        If the timestamp is zero or omitted, all directory entries are returned.

        :return: Dictionary representing result section of JSON response. Contains requested info about users
        '''
        return self._query(fields, series, iterator)

    def _query(self, fields: Optional[list[str]] = None, series: Optional[str] = None, iterator: Optional[int] = 0, *,
               method: str = "POST") -> dict:
        data: dict[str, Any] = {}
        if fields is not None:
            data["fields"] = fields
        if series is not None:
            data["series"] = series
        if iterator is not None:
            data["iterator"] = {"timestamp": iterator}
        files = {"blob-json": json.dumps(data).encode('utf-8')}
        return HipDevice.api_process_json_result(
            self.device.api_request(method, '/api/dir/query', files=files)
        )

    def put_validate(self, params=dict[str, Any]) -> None:
        '''
        function can validate a set of provided fields. If a field does not exist or
        provided value is not accepted, an error is reported to the caller.
        Available fields depend on the model type and can be obtained using the /api/dir/template function.

        :param params: A mandatory object with parameters to be validated, sent in the application/json format.
        :return: None
        '''

        files = {BlobType.DIR_NEW.value: json.dumps(params).encode('utf-8')}

        return HipDevice.api_process_json_success(
            self.device.api_put('/api/dir/validate', files=files)
        )
