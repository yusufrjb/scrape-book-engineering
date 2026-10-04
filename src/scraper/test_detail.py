import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

response = requests.get(url, timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

print("=== TITLE ===")
print(soup.select_one("h1").get_text(strip=True))

print("\n=== PRICE ===")
print(soup.select_one(".price_color").get_text(strip=True))

print("\n=== AVAILABILITY ===")
print(soup.select_one(".availability").get_text(" ", strip=True))