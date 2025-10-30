import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_top_skins(limit=10):
    url = "https://steamcommunity.com/market/search?appid=730"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    items = soup.find_all("a", class_="market_listing_row_link")

    skins = []
    for item in items[:limit]:
        name_el = item.find("span", class_="market_listing_item_name")
        price_el = item.find("span", class_="normal_price")

        name = name_el.text.strip() if name_el else "Unknown"
        price = price_el.text.strip() if price_el else "N/A"

        skins.append({"Name": name, "Price": price})

    df = pd.DataFrame(skins)
    df.to_csv("data/prices.csv", index=False)
    return df
