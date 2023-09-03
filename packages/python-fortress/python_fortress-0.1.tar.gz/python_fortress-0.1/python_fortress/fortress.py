import logging
from io import StringIO
from typing import Dict, Optional

import requests
from dotenv import dotenv_values, load_dotenv

# logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://www.passfortress.com/api/"


class Fortress:
    """
    A class that represents a secret fortress and allows you to interact with the API to retrieve an .env file.
    """

    def __init__(self, base_url: str = BASE_URL):
        """
        Initializes a Fortress instance.

        :param base_url: URL base para la API.
        """
        self.base_url = base_url
        self.api_key: str = ""
        self.access_token: str = ""
        self.master_key: str = ""
        self.envfile_name: str = ""
        self.headers: Dict[str, str] = {}
        self.load_fortress_credentials()
        self.load_headers()

    def load_fortress_credentials(self, dotenv_loader=dotenv_values) -> None:
        """
        Load credentials from environment variables using python-dotenv.
        """
        fortress_credentials = dotenv_loader()
        self.api_key = fortress_credentials.get("FORTRESS_API_KEY", "")
        self.access_token = fortress_credentials.get("FORTRESS_ACCESS_TOKEN", "")
        self.master_key = fortress_credentials.get("FORTRESS_MASTER_KEY", "")
        self.envfile_name = fortress_credentials.get("FORTRESS_ENVFILE_NAME", "")

    def load_headers(self) -> None:
        """
        Loads the necessary headers for API requests.
        """
        self.headers = {"Authorization": f"Bearer {self.access_token}"}

    def _build_url(self, endpoint: str) -> str:
        """
        Constructs the full URL for a specific endpoint.

        :param endpoint: desired endpoint.
        :return: full url.
        """
        return f"{self.base_url}{endpoint}"

    def get_envfile(self) -> Optional[str]:
        """
        Gets the content of the .env file from the API.

        :return: Content of the .env file or None if there is an error.
        """
        url = self._build_url(endpoint="get-envfile/")
        data = {
            "api_key": self.api_key,
            "master_key": self.master_key,
            "envfile_name": self.envfile_name,
        }
        response = requests.post(url=url, data=data, headers=self.headers)
        if response.status_code == 200:
            return response.json().get("envfile_data", {}).get("value")

        logger.error(f"Error getting envfile. Code: {response.status_code}. message: {response.text}")
        return None

    def load_env(self):

        envfile = self.get_envfile()
        if envfile:
            load_dotenv(stream=StringIO(envfile))
            return True
        return False


def load_env():
    """
    Convenience function to load the variables from the .env file into the environment variables.
    """
    fortress = Fortress()
    fortress.load_env()
