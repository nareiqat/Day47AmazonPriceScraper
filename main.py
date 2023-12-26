from bs4 import BeautifulSoup
import requests
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

URL = "https://www.amazon.com/Sanabul-Core-Hybrid-Gloves-White/dp/B07KQLMBR1/?_encoding=UTF8&pd_rd_w=IpZaQ&content-id=amzn1.sym.35cab78c-35e3-4fc1-aab0-27eaa6c86063%3Aamzn1.symc.e5c80209-769f-4ade-a325-2eaec14b8e0e&pf_rd_p=35cab78c-35e3-4fc1-aab0-27eaa6c86063&pf_rd_r=6BT9C1V71T4311767ZR4&pd_rd_wg=5wdgZ&pd_rd_r=54c95080-d77e-494f-8af1-1cd0850e09d2&ref_=pd_gw_ci_mcx_mr_hp_atf_m&th=1"

# needs to be changed from time to time to avoid amazon blocking request
header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
response = requests.get(URL, headers=header)

page_html = response.text

soup = BeautifulSoup(page_html, "html.parser")

price = soup.find("span", class_="a-offscreen").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)

item_name = soup.find("span", id="productTitle").get_text().split("|")[0]

GMAIL = os.environ.get("GMAIL")
PASSWORD = os.environ.get("PASSWORD")

if price_as_float < 30:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=GMAIL, password=PASSWORD)
        connection.sendmail(from_addr=GMAIL, to_addrs="anyemail@gmail.com",
                        msg=f"Subject: Price Alert!\n\n{item_name} - is now at ${price_as_float}")
#
