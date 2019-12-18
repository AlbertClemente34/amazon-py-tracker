import requests
from bs4 import BeautifulSoup
import re


def extract_url(url):
    if url.find("www.amazon.es") != -1:
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://www.amazon.es" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://www.amazon.es" + url[index:index2]
            else:
                url = None
    else:
        url = None
    return url

def get_converted_price(price):
    stripped_price = price.strip(" €,")
    replaced_price = stripped_price.replace(".", "")
    find_decimal = replaced_price.find(",")
    to_convert_price = replaced_price[0:find_decimal]
    converted_price = int(to_convert_price)
    return converted_price

def get_product_details(url):
    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept-Encoding":"gzip, deflate",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT":"1","Connection":"close",
        "Upgrade-Insecure-Requests":"1"
        }
    details = {"name": "","price": 0,"deal": True,"url": ""}
    _url = extract_url(url)

    if _url == "":
        details = None
    else:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "html5lib")
        title = soup.find(id="productTitle")
        price = soup.find(id="priceblock_dealprice")
        if price is None:
            price = soup.find(id="priceblock_ourprice")
            details["deal"] = False
        if title is not None and price is not None:
            details["name"] = title.get_text().strip()
            details["price"] = get_converted_price(price.get_text())
            details["url"] = _url
        else:
            return None
    return details

print(get_product_details("https://www.amazon.es/Logitech-G933-Artemis-Spectrum-inal%C3%A1mbricos/dp/B015HG77FC/ref=zg_bs_computers_14?_encoding=UTF8&psc=1&refRID=TD94K5DGHDRPJHXHPAYM"))