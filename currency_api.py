import requests

def get_exchange_rate(from_currency, to_currency, amount):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)  # ✅ Correct method
    data = response.json()
    
    if "rates" in data and to_currency in data["rates"]:
        return amount * data["rates"][to_currency]
    
    return "Conversion Error"
