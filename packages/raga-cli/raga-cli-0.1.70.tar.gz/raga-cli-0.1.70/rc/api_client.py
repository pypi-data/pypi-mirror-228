import json
from urllib.parse import urlparse
import requests
import logging
from rc.api import api_version


from rc.exceptions import RcException

logger = logging.getLogger(__name__)


RC_API_VERSION = api_version()

class APIClientError(RcException):
    def __init__(self, msg):
        super().__init__(msg)

class APIClient:
    def __init__(self, base_url, headers=None):
        self.base_url = self.validate_base_url(base_url)
        default_headers = {'Content-Type': 'application/json'}
        if headers:
            self.headers = {**default_headers, **headers}
        else:
            self.headers = default_headers

    def validate_base_url(self, base_url: str) -> str:
        parsed_url = urlparse(base_url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise APIClientError("Invalid base URL. Must be in the format 'http(s)://domain.com'.")
        return base_url

    def _make_request(self, method, endpoint, params=None, data=None):
        url = f"{self.base_url}/{RC_API_VERSION}/api/{endpoint}"
        logger.debug(f"API URL {url}")
        logger.debug(f"API ENDPOINT {endpoint}")
        logger.debug(f"API PARAMS {json.dumps(params)}")
        logger.debug(f"API PAYLOAD {json.dumps(data)}")
        logger.debug(f"API HEADER {json.dumps(self.headers)}")
        try:
            response = requests.request(method, url, params=params, headers=self.headers, data=data)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise APIClientError('Error occurred during HTTP request: {}'.format(e))
        except ValueError as e:
            raise APIClientError('Error occurred while parsing response JSON: {}'.format(e))

    def get(self, endpoint, data=None):
        return self._make_request("GET", endpoint, params=data)

    def post(self, endpoint, data=None):
        return self._make_request("POST", endpoint, data=data)

    def put(self, endpoint, data=None):
        return self._make_request("PUT", endpoint, data=data)

    def delete(self, endpoint):
        return self._make_request("DELETE", endpoint)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass  # You can perform cleanup actions here if needed
