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
        self.say("MCRcon Donation Tracking Started")
        pass

    def set_world_border(self, size: int):
        print(f"set_world_border({size})")
        self.__mcr.command(f"/worldborder set {size}")
        self.title(f"\"World Border is now {round(size)} blocks wide!\"")

    def announce_donation(self, donation: Donation):
        amount = format(donation.gbp_amount, ".2f")
        self.title('["",{"text":"' + donation.name + '","bold":true,"color":"dark_aqua"},{"text":" donated "},{"text":"£' + amount + '","bold":true,"color":"gold"},{"text":"!","bold":true},{"text":" Thank you!"}]', "subtitle")
        self.__mcr.command('/tellraw @a ["",{"text":"' + donation.name + '","bold":true,"color":"dark_aqua"},{"text":" donated "},{"text":"£' + amount + '","bold":true,"color":"gold"},{"text":"!","bold":true},{"text":" Thank you!"}]')

    def title(self, component, detail = "title", targets = "@a"):
        """
        Controls text displayed on the screen.
        :param detail: "clear", "reset", "subtitle", "title", "actionbar", or "times"
        :param targets: Specifies the player(s) to display a screen title to. Must be a player name, a target selector
        or a UUID. And the target selector must be of player type.
        :param component: Specifies the text to display as a title, subtitle, or on the action bar. Must be a valid text
        component.
        """
        print(f"Running /title {detail} {targets} {component}")
        #self.say(f"\"Running /title {targets} {detail} {component}\"")
        self.__mcr.command(f"/title {targets} {detail} {component}")

    def say(self, component):
        self.__mcr.command(f"/say {component}")

    def disconnect(self):
        """
        Disconnect from MCRcon
        """
        print("Disconnecting from MCRcon")
        self.__mcr.disconnect()
        del self

