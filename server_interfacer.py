from donation import Donation


class ServerInterfacer:
    """
    Interface for interacting with the Minecraft server
    """

    def __init__(self):
        pass

    def set_world_border(self, size: int):
        print(f"set_world_border({size})")
        self.show_title(f"World Border is now {round(size)} blocks wide!")

    def announce_donation(self, donation: Donation):
        self.show_title(f"{donation.name} donated £{donation.gbp_amount}! Thank you!")

    def show_title(self, title: str):
        print(f"show_title({title})")

