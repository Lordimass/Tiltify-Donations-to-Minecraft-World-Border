from currency_converter import CurrencyConverter
from tiltify_api_wrapper import Tiltify


class Donation:
    __converter = CurrencyConverter("gbp")

    def __init__(self, amount: int, currency: str, name: str, comment: str):
        self.amount = amount
        self.currency = currency
        self.name = name
        self.comment = comment
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
                int(d.get("amount").get("value")),
                d.get("amount").get("currency"),
                d.get("donor_name"),
                d.get("donor_comment")
            ))
        return donations

    def __repr__(self):
        return f"{self.name} donated £{self.gbp_amount}"