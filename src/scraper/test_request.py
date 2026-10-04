import requests

url = "https://books.toscrape.com/"
response = requests.get(url, timeout=10)

print(response.status_code)
print(response.url)