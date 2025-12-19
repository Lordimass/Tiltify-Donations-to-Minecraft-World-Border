import os

from dotenv import load_dotenv

# Load environment variables from `.env`
load_dotenv()

class Tiltify:
    """
    Wrapper class for the Tiltify API
    """

    __API_URL = "https://v5api.tiltify.com/api/public/"

    def __init__(self):
        self.__setup_environment_variables()

    def __setup_environment_variables(self):
        """
        Check whether the required environment variables were defined.
        """
        self.__CLIENT_ID = os.getenv("TILTIFY_CLIENT_ID")
        self.__CLIENT_SECRET = os.getenv("TILTIFY_CLIENT_SECRET")
        if self.__CLIENT_ID is None:
            raise EnvironmentError("Missing TILTIFY_CLIENT_ID in .env")
        elif self.__CLIENT_SECRET is None:
            raise EnvironmentError("Missing TILTIFY_CLIENT_SECRET in .env")
