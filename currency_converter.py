import requests

class CurrencyConverter:
    """
    Utility class to convert between currencies.
    From: https://www.geeksforgeeks.org/python/currency-converter-in-python/
    """

    def __init__(self, from_currency):
        # Fetching real-time data from the API
        data = (requests
                .get(
            f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{from_currency.lower()}.min.json")
                .json())
        self.from_currency = from_currency.lower()
        self.rates = data[self.from_currency]

    def convert(self, to_currency: str, amount: float) -> float:
        """Convert amount to another currency."""
        return round(amount * self.rates[to_currency.lower()], 2)

    def convert_backwards(self, from_currency: str, amount: float) -> float:
        """Convert amount from another currency to the base currency."""
        return round(amount / self.rates[from_currency.lower()], 2)
