class ServerInterfacer:
    """
    Interface for interacting with the Minecraft server
    """

    def __init__(self):
        pass

    def set_world_border(self, size: int):
        self.show_title(f"World Border is now {size} blocks wide!")
        print(f"set_world_border({size})")

    def show_title(self, title: str):
        print(f"show_title({title})")