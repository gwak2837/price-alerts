import os
import sys
import time
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException

# Add modules in common/functions.py - will be deprecated
sys.path.append(os.path.dirname(os.getcwd()))

from common.functions import Chrome

PRODUCT_URL = "https://badblood.co.kr/product/w-knt20-004%EB%B2%A0%EC%8B%9C-%EB%A1%B1%EC%8A%AC%EB%A6%AC%EB%B8%8C-%ED%8F%B4%EB%A1%9C-%EB%8B%88%ED%8A%B8/7886/category/558/display/1/#anchor1"
PRICE_CSS_SELECTOR = "#span_product_price_text"
COLORS_CSS_SELECTOR = (
    "#contents > div.container2 > div.item2 > div > div > table > tbody:nth-child(3) > tr > td > ul > li"
)
SIZES_CSS_SELECTOR = "#product_option_id2 > option"
COLOR = "블랙"
SIZE = "S"

badblood_chrome = Chrome()

while True:
    badblood_chrome.go_to_page(PRODUCT_URL)

    price = badblood_chrome.get_bs4_element(PRICE_CSS_SELECTOR)
    print(price.string)

    colors = badblood_chrome.driver.find_elements_by_css_selector(COLORS_CSS_SELECTOR)
    color_find = False
    for color in colors:
        if color.get_attribute("title") == COLOR:
            color_find = True
            if color.get_attribute("class") != "ec-product-selected":
                color.click()
                break
    if not color_find:
        print("해당 색상의 제품이 없습니다.")
        continue

    sizes = badblood_chrome.get_bs4_elements(SIZES_CSS_SELECTOR)
    size_find = False
    for size in sizes:
        if size.string.startswith(SIZE):
            size_find = True
            if size.string.find("품절") == -1:
                print(SIZE + " 재고가 있습니다.")
            else:
                print(SIZE + " 재고가 없습니다.")
    if not size_find:
        print("해당하는 사이즈가 없습니다.")

    time.sleep(10)

