from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.touch_actions import TouchActions as TA
from selenium.common.exceptions import *
import os
import time
import json
from lxml import html
from lxml.cssselect import CSSSelector
import math

# ======================================================================

class URLImageCrawler:
    def __init__(self):
        self.is_close_driver = False
        self.btn_show_more = None
        self.div_selector = CSSSelector("#search-unified-content .photo-list-photo-view")
        self.init_driver()
        self.ta = TA(self.driver)

    def init_driver(self):
        option = webdriver.ChromeOptions()
        option.add_argument("start-maximized")
        self.driver = webdriver.Chrome(chrome_options=option)

    def close_driver(self):
        if not self.is_close_driver:
            # self.driver.close()
            os.system("taskkill /f /im chromedriver.exe")
            print("[ * ] Close driver done")
            self.is_close_driver = True

    def is_display_btn_show_more(self):
        try:
            self.btn_show_more = self.driver.find_element(By.CSS_SELECTOR, ".infinite-scroll-load-more button")
            # print("[ * ] Btn show more is displayed")
            return True
        except:
            return False

    def write_urls(self, keyword, urls, path='./Data'):
        out_path = os.path.abspath(os.path.join(path, keyword + ".txt"))
        with open(out_path, 'w') as f:
            f.write('\n'.join(urls))
        print("[ + ] Finish write {} urls to {}".format(len(urls), out_path))

    def crawl_background_links(self, keyword_search, num_scroll=5):
        start_time = time.clock()
        driver = self.driver
        url = "https://www.flickr.com/search/?text={}".format(keyword_search)
        driver.get(url)

        base_url = "https:"
        urls = []

        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "#search-unified-content .photo-list-photo-view"
                ))
            )
        except Exception as e:
            print("[ @ ] Exception: ", e)
            return

        try:
            a_elm = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "#search-unified-content a[class~='view-more-link']"
                ))
            )
            text_str = a_elm.get_attribute("innerHTML")[len("View all "):]
            total_images_str = ''.join(text_str.split(','))
            total_images = int(total_images_str)
            num_scroll = int(math.floor(total_images / 300))
            print("[ * ] key word {}: {} total images - {} scroll".format(keyword, total_images, num_scroll))
        except Exception as e:
            print("[ - ] Exception: ", e)


        # scroll
        for _ in range(num_scroll):
            print("[ * ] {}: scroll {}".format(keyword, _ + 1))
            self.ta.scroll(0, 2000).perform()
            if self.is_display_btn_show_more():
                self.btn_show_more.click()

        root = html.fromstring(driver.page_source)
        div_elms = self.div_selector(root)
        # div_elms = driver.find_elements(By.CSS_SELECTOR, "#search-unified-content .photo-list-photo-view")
        # print("div_elms len = ", len(div_elms))
        for div_elm in div_elms:
            # value = div_elm.value_of_css_property('background-image')
            style = div_elm.attrib['style']
            start_index = style.find("url(")
            if start_index >= 0:
                end_index = style.find('")', start_index)
                url = style[start_index + 5: end_index]
                urls.append(base_url + url)


        end_time = time.clock()
        print("[ * ] {}: Collected {} urls => {} seconds".format(
            keyword_search, len(urls), end_time - start_time)
        )

        self.write_urls(keyword_search, urls)

if __name__ == '__main__':
    keywords = []
    # keywords.append("The Huc Bridge")
    # keywords.append("Hoan Kiem Lake")
    # keywords.append("Thap Rua Tower")
    # keywords.append("Post Office Ha Noi")

    # keywords.append("Quan Thanh Temple")
    # keywords.append("Tran Quoc Pagoda")
    # keywords.append("West Lake Ha Noi")

    urlImageCrawler = URLImageCrawler()

    for keyword in keywords:
        urlImageCrawler.crawl_background_links(keyword_search=keyword, num_scroll=4)

    urlImageCrawler.close_driver()