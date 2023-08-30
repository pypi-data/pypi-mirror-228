from typing import (
    TYPE_CHECKING
)

from rc.config import Config
from rc.api_client import APIClient, APIClientError
# if TYPE_CHECKING:


def get_repository(config:Config, repo_name):
    with APIClient(config.get_core_config_value("rc_base_url")) as client:
            response = client.get(f"repos-name?repoName={repo_name}")
            if response:
                data = response.json()
                data = data.get('data', None)
                if data and "repo_name" in data and "tag" in data:
                    return data['repo_name'], data['tag']
                else:
                    return False, False
            else:
                raise APIClientError(f"something went wrong")