import threading
import time
from typing import List
from donation import Donation
from server_interfacer import ServerInterfacer
from structure import Structure
from tiltify_api_wrapper import Tiltify

class Main:
    SERVER_HOST_IP = "192.168.30.35"
    SERVER_HOST_PORT = 25575

    CAMPAIGN_ID = "f7b5df80-5148-42ed-8ae6-6588e0d72aaa"
    GBP_PER_BLOCK = 1
    TIME_BETWEEN_DONATION_CHECKS = 10

    def __init__(self):
        self.__check_donations_thread = None
        self.tiltify = Tiltify(Main.CAMPAIGN_ID)
        self.server_interfacer = ServerInterfacer(Main.SERVER_HOST_IP, Main.SERVER_HOST_PORT)

        self.structures = Structure.get_structure_list("assets/structures.csv")
        self.donations: List[Donation] = Donation.get_all_donations(Main.CAMPAIGN_ID)

        self.total_raised = Donation.get_total_raised(self.donations)

        self.server_interfacer.set_world_border(self.total_raised / Main.GBP_PER_BLOCK)
        self.server_interfacer.announce_donation(self.donations[-1])

        time.sleep(Main.TIME_BETWEEN_DONATION_CHECKS)
        threading.Thread(target=self.continually_check_donations).start()

    def continually_check_donations(self):
        while True:
            if (self.__check_donations_thread is None) or (not self.__check_donations_thread.is_alive()):
                self.__check_donations_thread = threading.Thread(target=self.check_donations)
                self.__check_donations_thread.start()

    def check_donations(self):
        fresh_donos: List[Donation] = Donation.get_all_donations(Main.CAMPAIGN_ID)
        new_donos = []

        # Filter for new donations
        for fresh_dono in fresh_donos:
            found = False
            for existing_dono in self.donations:
                if fresh_dono == existing_dono:
                    found = True
                    break
            if not found:
                new_donos.append(fresh_dono)
                self.server_interfacer.announce_donation(fresh_dono)
                self.total_raised += fresh_dono.gbp_amount
                self.server_interfacer.set_world_border(self.total_raised / Main.GBP_PER_BLOCK)
                time.sleep(5)
        self.donations = fresh_donos

        if len(new_donos) == 0:
            print("Found no new donations.")

        time.sleep(Main.TIME_BETWEEN_DONATION_CHECKS)

if __name__ == "__main__":
    Main()