from currency_converter import CurrencyConverter
from tiltify_api_wrapper import Tiltify

class Main:
    CAMPAIGN_ID = "d36d4806-dc16-4d4d-917d-1df450da39ce"  # Fake ID for testing
    # CAMPAIGN_ID = "f7b5df80-5148-42ed-8ae6-6588e0d72aaa" # Production Campaign ID
    GBP_PER_BLOCK = 1

    def __init__(self):
        tiltify = Tiltify(Main.CAMPAIGN_ID)
        donations = tiltify.list_donations("", "")
        print(len(donations))

        converter = CurrencyConverter("gbp")
        for donation in donations:
            print(f"{donation.get("donor_name")}" +
                  f" donated £" +
                  f"{converter.convert_backwards(
                      donation.get("amount").get("currency"), 
                      float(donation.get("amount").get("value"))
                  )} ({donation.get("amount").get("value")} {donation.get("amount").get("currency")})")

if __name__ == "__main__":
    Main()