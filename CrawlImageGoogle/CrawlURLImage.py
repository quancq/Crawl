# Input :   file path contain keyword search list
#           output file path
# Output:   files contain url list
# ------------------------------------------------

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.touch_actions import TouchActions as TA
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
import os
import time
import json
from lxml import html
from lxml.cssselect import CSSSelector

class URLImageCrawler:

    def __init__(self):
        self.keywords = []
        self.wait_time_per_img = 0.5                          # seconds wait 1 image loaded
        self.max_num_continuous_scroll_per_img = 1          # if num scroll order to load 1 image exceed max_num then stop crawl

        self.init_driver()
        self.btn_show_more = None
        self.father_div = None
        self.country_div = None
        self.div_url_selector = CSSSelector("#rg .rg_di .rg_meta")
        print("[ * ] Init URLImageCrawler object done")


    def init_driver(self, url='https://images.google.com/'):
        try:
            # disable load image in browser
            option = webdriver.ChromeOptions()
            # prefs = {}
            # prefs["profile.managed_default_content_settings.image"] = 2
            # option.add_experimental_option("prefs", prefs)
            option.add_argument("start-maximized")
            # option.add_argument("user-data-dir=C:\\Users\\ad\\AppData\\Local\Google\\Chrome\\User Data\\Profile 1")

            self.driver = webdriver.Chrome(chrome_options=option)
            driver = self.driver
            self.ta = TA(self.driver)

            driver.get(url)
            print("[ * ] Current driver url : ", url)

            self.txt_search = driver.find_element_by_id("lst-ib")
            # print("[ ? ] Input search elment : ", self.txt_search)
            self.btn_search = driver.find_elements_by_css_selector("#searchform button[name='btnG'][type='submit']")[0]
            # print("[ ? ] Button submit search : ", self.btn_search)
            # self.country_div = driver.find_element_by_id("fbarcnt")
            # print("[ ? ] Country div : ", self.country_div)

        except Exception as e:
            print("[@@@] Exception : ", e)

    def init_again(self):
        # self.btn_show_more = self.driver.find_element(By.ID, "smb")
        self.txt_search = self.driver.find_element_by_id("lst-ib")
        self.txt_search.clear()

    def close_driver(self):
        # self.driver.close()
        os.system("taskkill /f /im chromedriver.exe")
        print("[ * ] Close driver done")

    def read_file(self, intput_path='./Data/Search_List.txt'):
        '''
        :param path: link to file contain search list
        :return: list contain keywords
        '''

        with open(intput_path, 'r', encoding='utf-8') as f:
            keywords = f.read().strip().split('\n')

        self.keywords.extend(keywords)
        print("[ + ] Read file {} done => Collected {} new keywords".format(intput_path, len(keywords)))
        print("New keywords : ", keywords)
        print('[ * ] Current keywords : ', self.keywords)
        return keywords

    def write_file(self, keyword, urls, output_path='./Data/'):
        dir_path = os.path.join(os.path.abspath(output_path), keyword)
        if not os.path.exists(dir_path) or os.path.isfile(dir_path):
            os.mkdir(dir_path)
        path = os.path.join(dir_path, keyword + '-{}.txt'.format(time.time()))

        print("[ * ] Write file {} started".format(path))
        with open(path, 'w') as f:
            f.write('\n'.join(urls))
        print("[ + ] Write file {} : {} urls".format(path, len(urls)))

    def crawl_url_image(self, crawl_more=True, search_path='./Data/Search_List.txt', output_path='./Data'):
        try:
            driver = self.driver
            keywords = self.read_file(search_path)
            keywords = [keywords[0]]

            for keyword in keywords:
                # Crawl image urls of keyword
                start_time = time.clock()

                self.txt_search.send_keys(keyword)
                self.btn_search.click()
                if self.btn_show_more is None:
                    self.btn_show_more = driver.find_element(By.ID, "smb")
                if self.father_div is None:
                    self.father_div = driver.find_element(By.ID, "rg")

                urls = []
                num_continuous_scroll = 0

                self.ta.scroll(0, 14000).perform()
                while not self.btn_show_more.is_displayed():
                    self.ta.scroll(0, 2000).perform()
                if crawl_more:
                    self.btn_show_more.click()
                    self.ta.scroll(0, 3000).perform()

                    root = html.fromstring(driver.page_source)
                    div_url_images = self.div_url_selector(root)
                    print("[ * ] Current loaded {} urls".format(len(div_url_images)))
                    wait_img_id = len(div_url_images)

                    while num_continuous_scroll <= self.max_num_continuous_scroll_per_img:
                        # Wait load images
                        try:
                            print("Wait id ", wait_img_id)
                            div_url_image = WebDriverWait(driver, self.wait_time_per_img).until(
                                EC.presence_of_element_located((
                                    By.CSS_SELECTOR,
                                    "div#rg [data-ri='{}'][class~='rg_di'] [class~='rg_meta']".format(wait_img_id))
                                )
                            )
                            # load image successful
                            # div_url_images = self.father_div.find_elements(By.CSS_SELECTOR, "[class~='rg_di'] [class~='rg_meta']")

                            # use lxml library order to parser
                            # root = html.fromstring(driver.page_source)
                            # div_url_images = self.div_url_selector(root)

                            self.ta.scroll(0, 4000).perform()
                            num_continuous_scroll = 0
                            wait_img_id += 70
                            # wait_img_id = len(div_url_images)
                            # print("Loaded number URL = ", wait_img_id - 1)


                        except:
                            # if num_continuous_scroll == 0:
                            #     wait_img_id -= 30
                            num_continuous_scroll += 1
                            print("[@@@] Khong load dc image")
                            # if self.btn_show_more.is_displayed():
                            #     self.btn_show_more.click()
                        # finally:
                            # if num_continuous_scroll == self.max_num_continuous_scroll_per_img:
                            #     self.ta.scroll(0, 2000).perform()

                print("[ * ] Crawl url of {} done".format(keyword))
                # urls = [json.loads(div.get_attribute("innerText")).get('ou', []) for div in div_url_images]

                root = html.fromstring(driver.page_source)
                div_url_images = self.div_url_selector(root)
                urls = [json.loads(div.text).get('ou', []) for div in div_url_images]
                self.write_file(keyword, urls, output_path)

                end_time = time.clock()
                print("[ * ] Crawl Time for {} is : {} seconds".format(keyword, (end_time - start_time)))

        finally:
            self.close_driver()


    def crawl_url_image1(self, crawl_more=True, search_path='./Data/Search_List.txt', output_path='./Data'):
        try:
            driver = self.driver
            keywords = self.read_file(search_path)
            # keywords = [keywords[0]]

            for keyword in keywords:
                # Crawl image urls of keyword
                start_time = time.clock()
                self.init_again()
                self.txt_search.send_keys(keyword)
                self.txt_search.send_keys(Keys.ENTER)
                # self.btn_search.click()

                # if self.btn_show_more is None:
                self.btn_show_more = driver.find_element(By.ID, "smb")
                if self.father_div is None:
                    self.father_div = driver.find_element(By.ID, "rg")
                if self.country_div is None:
                    self.country_div = driver.find_element_by_id("fbarcnt")

                urls = []
                num_continuous_scroll = 0

                self.ta.scroll(0, 14000).perform()
                while not self.btn_show_more.is_displayed():
                    self.ta.scroll(0, 2000).perform()
                if crawl_more:
                    self.btn_show_more.click()
                    while not self.country_div.is_displayed():
                        self.ta.scroll(0, 2000).perform()
                    WebDriverWait(driver, 1)

                    # root = html.fromstring(driver.page_source)
                    # div_url_images = self.div_url_selector(root)
                    # print("[ * ] Current loaded {} urls".format(len(div_url_images)))
                    # wait_img_id = len(div_url_images)



                print("[ * ] Crawl url of {} done".format(keyword))
                # urls = [json.loads(div.get_attribute("innerText")).get('ou', []) for div in div_url_images]

                root = html.fromstring(driver.page_source)
                div_url_images = self.div_url_selector(root)
                urls = [json.loads(div.text).get('ou', []) for div in div_url_images]
                self.write_file(keyword, urls, output_path)

                end_time = time.clock()
                print("[ * ] Crawl Time for {} is : {} seconds".format(keyword, (end_time - start_time)))

        finally:
            self.close_driver()


if __name__ == '__main__':
    urlImageCrawler = URLImageCrawler()
    urlImageCrawler.crawl_url_image1(crawl_more=False)
