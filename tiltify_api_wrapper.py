import json
import os

import requests
from dotenv import load_dotenv
from urllib3.util import Url

# Load environment variables from `.env`
load_dotenv()

class Tiltify:
    """
    Wrapper class for the Tiltify API
    """

    __API_URL = "https://v5api.tiltify.com/"

    def __init__(self, campaign_id):
        self.__setup_environment_variables()
        self.campaign_id = campaign_id

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

    def __get_application_access_token(self):
        """
        Generate a new Application Access Token
        :return: The application access token
        """
        response = requests.post(
            f"{Tiltify.__API_URL}oauth/token",
            headers={
                "Content-Type": "application/json"
            },
            json={
                "client_id": self.__CLIENT_ID,
                "client_secret": self.__CLIENT_SECRET,
                "grant_type": "client_credentials",
                "scope": "public"
            }
        )
        if not response.ok:
            raise RuntimeError(f"Response when fetching application access token was not OK:\n{response}")
        else:
            return response.json()["access_token"]

    def list_donations(self, completed_before = "", completed_after = ""):
        """
        List all the donations between two dates.

        :param completed_before: An ISO Date String representing the start of the date range to fetch donations from.
        :param completed_after: An ISO Date String representing the end of the date range to fetch donations from.
        :return: A list of objects representing the donations in the given date range.
        """
        access_token = self.__get_application_access_token()
        response = requests.get(
            f"{Tiltify.__API_URL}api/public/campaigns/{self.campaign_id}/donations?completed_before={completed_before}&completed_after={completed_after}&limit=100",
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
        if not response.ok:
            raise RuntimeError(f"Response when fetching donation list was not OK:\n{response}")
        elif response.json().get("metadata").get("after") is not None:
            return response.json().get("data") + self.__list_donations_after(
                response.json().get("metadata").get("after"),
                access_token
            )
        else:
            return response.json().get("data")

    def __list_donations_after(self, after, access_token):
        response = requests.get(
            f"{Tiltify.__API_URL}api/public/campaigns/{self.campaign_id}/donations?after={after}&limit=100",
            headers={
                "Authorization": f"Bearer {access_token}"
            }
        )
        if not response.ok:
            raise RuntimeError(f"Response when fetching donation list was not OK:\n{response}")
        elif response.json().get("metadata").get("after") is not None:
            return response.json().get("data") + self.__list_donations_after(
                response.json().get("metadata").get("after"),
                access_token
            )
        else:
            return response.json().get("data")

