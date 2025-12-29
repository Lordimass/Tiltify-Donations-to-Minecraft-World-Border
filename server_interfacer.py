import os

from donation import Donation
from mcrcon import MCRcon

class ServerInterfacer:
    """
    Interface for interacting with the Minecraft server
    """

    def __init__(self, host: str, port: int):
        password = self.__CLIENT_ID = os.getenv("MC_RCON_PASSWORD")
        if password is None:
            raise EnvironmentError("Missing MC_RCON_PASSWORD in .env")
        self.__mcr = MCRcon(host, password, port)
        self.__mcr.connect()
        resp = self.__mcr.command("/say MCRcon Test!")
        print(resp)
        pass

    def set_world_border(self, size: int):
        print(f"set_world_border({size})")
        self.show_title(f"World Border is now {round(size)} blocks wide!")

    def announce_donation(self, donation: Donation):
        self.show_title(f"{donation.name} donated £{donation.gbp_amount}! Thank you!")

    def show_title(self, title: str):
        print(f"show_title({title})")

    def disconnect(self):
        """
        Disconnect from MCRcon
        """
        print("Disconnecting from MCRcon")
        self.__mcr.disconnect()
        del self

