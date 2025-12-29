import csv

class Structure:
    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.x = x
        self.y = y

    @staticmethod
    def get_structure_list(structure_list_path: str):
        """
        Get a list of Structure objects from a given file.
        :param structure_list_path:
        :return:
        """
        lines = []
        with open(structure_list_path, newline="") as f:
            reader = csv.reader(f)
            lines = [row for row in reader]
            lines.pop(0) # Remove column titles

        structures = []
        for line in lines:
            structures.append(Structure(line[0], int(line[1]), int(line[2])))
        return structures

    @staticmethod
    def get_structures_in_range(structures: list, ran: tuple[int, int], origin: tuple[int, int] = (0, 0)):
        """
        Returns a list of structures within a certain range of blocks from `origin`. Distance is measured using the
        Manhattan metric.
        :param structures: The list of structures to filter from
        :param ran: A tuple containing (minimum distance [inclusive], maximum distance [exclusive])
        :param origin: The coordinates of the origin of the area to search.
        :return: A list of structures in range.
        """
        in_range = []
        for structure in structures:
            distance_from_origin = abs(structure.x - origin[0]) + abs(structure.y - origin[1])
            if ran[1] >= distance_from_origin > ran[0]:
                in_range.append(structure)
        return in_range

    def __repr__(self):
        return f"{self.get_pretty_structure_name()} at ({self.x}, {self.y})"

    def get_pretty_structure_name(self):
        """
        Get the user presentable name of the structure. i.e. `minecraft:ruined_portal` -> `Ruined Portal`
        :return: A string representing the name of the structure
        """
        return (self.name # minecraft:ruined_portal
            .split(":")[1] # ruined_portal
            .replace("_", " ") # ruined portal
            .title() # Ruined Portal
        )