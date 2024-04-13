import asyncio
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from config import *


async def parser_html(html):
    try:
        soup = BeautifulSoup(html, 'html.parser')

        news_list = list()

        news_elements = soup.find_all("div", class_="style_NewsItemRoot__3nhHX css-vurnku")
        count = 1
        for news in news_elements:
            short_description = news.find('h3', {'data-bn-type': 'text'}).text
            news_link = "https://www.binance.com" + news.find('a')['href']

            if count == 1:
                res = "1️⃣ [{}]({})".format(short_description, news_link)
            elif count == 2:
                res = "2️⃣ [{}]({})".format(short_description, news_link)
            elif count == 3:
                res = "3️⃣ [{}]({})".format(short_description, news_link)
            elif count == 4:
                res = "4️⃣ [{}]({})".format(short_description, news_link)
            elif count == 5:
                res = "5️⃣ [{}]({})".format(short_description, news_link)
            elif count == 6:
                res = "6️⃣ [{}]({})".format(short_description, news_link)
            elif count == 7:
                res = "7️⃣ [{}]({})".format(short_description, news_link)
            elif count == 8:
                res = "8️⃣ [{}]({})".format(short_description, news_link)
            elif count == 9:
                res = "9️⃣ [{}]({})".format(short_description, news_link)
            elif count == 10:
                res = "🔟 [{}]({})".format(short_description, news_link)


            if count > 10:
                pass
            else:
                news_list.append(res)
            count += 1


        return news_list
    except Exception as error:
        print(error)
        print("Error in parser_html()")


async def scrap_binance():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver_service = Service(ChromeDriverManager().install())

        driver = webdriver.Chrome(service=driver_service, options=chrome_options)

        try:
            driver.get("https://www.binance.com/en/feed/news/all")
            html = driver.page_source
            news_list = await parser_html(html)
            return news_list
        finally:
            driver.quit()
    except Exception as error:
        print(error)
        print("Error in scrap_binance()")


# async def token_data():
#     url = "https://api.coingecko.com/api/v3/coins/ethereum/contract/0xdac17f958d2ee523a2206206994597c13d831ec7"
#
#     headers = {"x-cg-pro-api-key": "CG-dB9Z75TH2WHQ1uDihyRamBKu"}
#
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         print(response.json())
#     else:
#         print(response)

