from currency_converter import CurrencyConverter
from tiltify_api_wrapper import Tiltify

class Donation:
    __converter = CurrencyConverter("gbp")

    def __init__(self, amount: float, currency: str, name: str, comment: str, id: str):
        self.amount = amount
        self.currency = currency
        self.name = name
        self.comment = comment
        self.id = id
        self.gbp_amount = Donation.__converter.convert_backwards(currency, amount)

    @staticmethod
    def get_all_donations(campaign_id: str):
        """
        Get a list of all donations on the given campaign.
        :param campaign_id: The ID of the campaign to search for donations from
        :return: A list of donations
        """
        tiltify = Tiltify(campaign_id)
        response = tiltify.list_donations()
        donations = []
        for d in response:
            donations.append(Donation(
                float(d.get("amount").get("value")),
                d.get("amount").get("currency"),
                d.get("donor_name"),
                d.get("donor_comment"),
                d.get("id")
            ))
        return donations

    @staticmethod
    def get_total_raised(donations):
        total = 0
        for donation in donations:
            total += donation.gbp_amount
        return round(total, 2)

    def __repr__(self):
        return f"<Donation {self.id} | {self.name}, £{self.gbp_amount}>"

    def __eq__(self, other):
        return self.id == other.id