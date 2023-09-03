from json import JSONDecodeError

import requests

from ir_client.exceptions import AuthorizationFailedException, InvalidDataException, MappingException
from ir_client.utils.url_utils import build_absolute_url


class IracingClient:
    def __init__(self, protocol='https', host='members.iracing.com'):
        self.base_url = build_absolute_url(protocol, host)  # TODO get from config

    def get_raw_data(self, endpoint_type_cls, endpoint_parameters, session_parameters):
        endpoint_type = endpoint_type_cls()
        results = self._send_request(endpoint_type, endpoint_parameters, session_parameters)
        return endpoint_type.extract_data(results)

    def get_data(self, endpoint_type_cls, endpoint_parameters, session_parameters):
        endpoint_type = endpoint_type_cls()
        results = self._send_request(endpoint_type, endpoint_parameters, session_parameters)
        try:
            return endpoint_type.map_data(results)
        except (JSONDecodeError, MappingException) as e:
            raise InvalidDataException(endpoint_type_cls, endpoint_parameters, results.text[:1000]) from e
    
    def _send_request(self, endpoint_type, endpoint_parameters, session_parameters) -> requests.Response:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',  # TODO extract value
            'Cookie': f'irsso_membersv2={session_parameters.cookie_irsso_membersv2}',  # TODO use proper cookie
        }
        url = endpoint_type.url(self.base_url)
        results = requests.post(
            url=str(url), 
            headers=headers, 
            data=endpoint_parameters.as_dict(),
            allow_redirects=False
        )
        if self._has_authorization_failed(results):
            raise AuthorizationFailedException()
        return results

    def _has_authorization_failed(self, response: requests.Response):
        return response.status_code == 302 and (
            "login.jsp" in response.headers['Location'] or "notauthed.jsp" in response.headers['Location']
        )
