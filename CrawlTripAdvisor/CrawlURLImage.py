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

# ======================================================================

class URLImageCrawler:
    def __init__(self):
        self.countries = {}
        self.provinces = {}
        self.attractions = {}

        # self.attraction_url_selector = None
        self.attraction_url_selector = CSSSelector("#ATTR_ENTRY_.attraction_element .listing_title a")
        self.attraction_img_selector = CSSSelector("#taplc_pv_resp_content_hero_zepto_0 [class~='inHeroList'] div.tinyThumb")

        self.btn_next_list_attraction = None

        self.is_close_driver = False
        self.init_driver()

    def write_url(self, urls=[], output_path=None):
        if output_path is None:
            output_path = "./Data/Temp-{}.txt".format(time.time())

        print("[ * ] Write file {} started".format(output_path))
        with open(output_path, 'w') as f:
            f.write('\n'.join(urls))
        print("[ + ] Write file {} : {} urls".format(output_path, len(urls)))

    def write_map(self, map, output_path, split_character=','):
        print("[ * ] Write file {} started".format(output_path))
        # if not os.path.exists(output_path):
        #     self.create_dir_path(output_path)

        with open(output_path, 'w') as f:
            for name, url in map.items():
                f.write("{}{}{}\n".format(name, split_character, url))
        print("[ + ] Write file {} : {} urls".format(output_path, len(map)))

    def read_map(self, input_path):
        with open(input_path, 'w') as f:
            lst = f.read().strip().split('\n')

        map = {}
        for elm in lst:
            temp = elm.split(',')
            map.update({temp[0]: temp[1]})

        return map

    def init_driver(self):
        option = webdriver.ChromeOptions()
        option.add_argument("start-maximized")

        driver = webdriver.Chrome(chrome_options=option)
        self.driver = driver

    def close_driver(self):
        if not self.is_close_driver:
            # self.driver.close()
            os.system("taskkill /f /im chromedriver.exe")
            print("[ * ] Close driver done")
            self.is_close_driver = True

    def create_dir_path(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def crawl_attraction(self, url):
        driver = self.driver
        driver.get(url)

        url_images = []
        try:
            see_all_elm = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    ".carousel_images .see_all_count span"
                ))
            )
            see_all_elm.click()

            # crawl all url image
            elm = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((
                    By.ID,
                    "taplc_pv_resp_content_hero_zepto_0"
                ))
            )
            elm = elm.find_elements_by_css_selector("[data-totalthumbs]")[0]
            total_url_image = int(elm.get_attribute("data-totalthumbs"))

            btn_left = elm.find_elements_by_class_name("left")[0]
            btn_right = elm.find_elements_by_class_name("right")[0]

            # print("btn left = ", btn_left.get_attribute("class"))

            while "disabled" not in btn_left.get_attribute("class"):
                btn_left.click()

            # click btn right until loaded all url image
            while "disabled" not in btn_right.get_attribute("class"):
                btn_right.click()

            # wait for final image loaded
            try:
                print("[ * ] Waiting for image {} loaded".format(total_url_image - 1))
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        "#taplc_pv_resp_content_hero_zepto_0 [class~='inHeroList'] [data-offset='{}']"
                            .format(total_url_image - 1)
                    ))
                )
                print("[ * ] image {} loaded".format(total_url_image - 1))
                doc = html.fromstring(driver.page_source)
                img_elms = self.attraction_img_selector(doc)
                # print("img_elms: ", img_elms)

                url_images = [img_elm.attrib.get("data-bigurl", "") for img_elm in img_elms]

            except Exception as e:
                print("[@@@] Don't loaded final image in {}, Exception {}".format(url, e))

        except Exception as e:
            print("[@@@] Exception: ", e)

        print("[ * ] Attraction {}: collected {} url images".format(url, len(url_images)))
        return url_images

    def crawl_next_provinces(self, intput_url):
        driver = self.driver
        driver.get(intput_url)
        print("[ * ] Current driver url : ", intput_url)

        li_elms = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "#LOCATION_LIST ul.geoList li"
            ))
        )
        li_elms = driver.find_elements(By.CSS_SELECTOR, "#LOCATION_LIST ul.geoList li")
        map_province_name_with_url = {}
        urls = []
        for li_elm in li_elms:
            a_elm = li_elm.find_element_by_tag_name('a')
            province_name = li_elm.find_element_by_tag_name("span").get_attribute("innerText")
            url = a_elm.get_attribute("href")
            map_province_name_with_url.update({province_name: url})
            # urls.append(url)

        a_next = None
        try:
            a_next = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "#LOCATION_LIST .pgLinks a[class~='sprite-pageNext']"
                ))
            )
        except:
            next_link = None

        # a_next = driver.find_element(By.CSS_SELECTOR, "#pgLinks a.sprite-pageNext")
        if a_next is not None:
            next_link = a_next.get_attribute("href")

        print("[ * ] Crawl provinces page {}: collected {} urls, next link = {}".format(
            intput_url, len(map_province_name_with_url), next_link
        ))

        return map_province_name_with_url, next_link

    def crawl_province(self, start_url):
        def crawl_one_page(url, is_first_page=False):
            driver = self.driver
            if not is_first_page:
                driver.get(url)
                print("[ * ] Current driver url : ", url)

            # crawl current list attraction
            map_attraction_name_with_url = {}
            next_link = None

            # wait first attraction
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((
                        By.CSS_SELECTOR,
                        "#ATTR_ENTRY_.attraction_element a"
                    ))
                )
                try:
                    self.btn_next_list_attraction = driver.find_element(
                            By.CSS_SELECTOR, "#FILTERED_LIST .pagination a[class~='next']"
                    )
                    next_link = self.btn_next_list_attraction.get_attribute("href")
                except Exception as e:
                    print("[ @ ] Exception: ", e)

                # parse html to lxml library
                doc = html.fromstring(driver.page_source)
                doc.make_links_absolute("https://www.tripadvisor.com")
                # if self.attraction_url_selector is None:
                #     self.attraction_url_selector = CSSSelector("#ATTR_ENTRY_.attraction_element .listing_title a")

                a_elms = self.attraction_url_selector(doc)
                # print("a_elms: ", a_elms)
                map_attraction_name_with_url = {
                    a_elm.text: a_elm.attrib.get("href", "")
                    for a_elm in a_elms
                }
            except Exception as e:
                print("[ * ] Don't loaded ATTR_ENTRY_ in ", url)
                print("[@@@] exception: ", e)



            print("[ * ] Page {}: collected {} url".format(url, len(map_attraction_name_with_url)))
            return map_attraction_name_with_url, next_link

        driver = self.driver
        driver.get(start_url)
        print("[ * ] Current driver url : ", start_url)

        # crawl current list attraction
        map_attraction_name_with_url = {}
        map_attraction_name_with_url, next_link = crawl_one_page(start_url, is_first_page=True)

        map = {}
        while next_link is not None:
            map, next_link = crawl_one_page(next_link)
            map_attraction_name_with_url.update(map)

        # crawl pagination
        # a_elms = None
        # try:
        #     a_elms = WebDriverWait(driver, 2).until(
        #         EC.presence_of_element_located((
        #             By.CSS_SELECTOR,
        #             "#FILTERED_LIST [class='unified pagination '] a"
        #         ))
        #     )
        #     if self.btn_next_list_attraction is not None:
        #         self.btn_next_list_attraction = driver.find_element(By.CSS_SELECTOR, "#FILTERED_LIST .pagination a[class~='next']")
        # except:
        #     print("[ - ] Dont loaded (#FILTERED_LIST [class='unified pagination '] a)")
        #
        # links = []
        # if a_elms is not None:
        #     a_elms = driver.find_elements(By.CSS_SELECTOR, "#FILTERED_LIST [class='unified pagination '] a")
        #     links = [a_elm.get_attribute("href") for a_elm in a_elms]
        #
        #     # crawl list attraction in each link
        #     for link in links:
        #         map_attraction_name_with_url.update(crawl_one_page(link))

        print("[ * ] Page {}: collected {} url".format(start_url, len(map_attraction_name_with_url)))
        return map_attraction_name_with_url

    def crawl_country(self, keyword='VietNam'):
        try:
            driver = self.driver

            url = "https://www.tripadvisor.com/Attractions"
            driver.get(url)
            print("[ * ] Current driver url : ", url)

            txt_search = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "#taplc_trip_search_home_attractions_0 input.typeahead_input"
                ))
            )

            btn_search = WebDriverWait(driver, 1).until(
                EC.presence_of_element_located((
                    By.ID,
                    "SUBMIT_THINGS_TO_DO")
                )
            )

            txt_search.send_keys(keyword)
            btn_search.click()

            nav_list = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR,
                    "#taplc_attraction_filters_clarity_0 .ap_filter_wrap:last-child .navigation_list"
                ))
            )
            a_elms = nav_list.find_elements_by_tag_name('a')

            next_link = a_elms[-1].get_attribute("href")
            if a_elms[-1].get_attribute("innerText") == "More":
                next_link = a_elms[-1].get_attribute("href")
            else:
                next_link = None
            a_elms = a_elms[:-1]

            map_province_name_with_url = {}
            url = ""
            urls = []
            s = "Things to do in"
            for a_elm in a_elms:
                province_name = a_elm.get_attribute("innerText")[len(s) + 1:]
                url = a_elm.get_attribute("href")
                map_province_name_with_url.update({province_name: url})
                # urls.append(url)

            print("[ * ] Page 1 ({}): {} urls".format(driver.current_url, len(map_province_name_with_url)))

            # crawl all next provinces page
            while next_link is not None:
                map, next_link = self.crawl_next_provinces(next_link)
                map_province_name_with_url.update(map)
            self.countries.update({keyword: map_province_name_with_url})

            dir_path = "./Data/{}".format(keyword)
            self.create_dir_path(dir_path)
            path = "./Data/{}/Provinces of {}.txt".format(keyword, keyword)
            path = os.path.abspath(path)
            self.write_url(list(map_province_name_with_url.values()), output_path=path)
            # driver.save_screenshot('./Data/temp.png')

            # self.close_driver()
        except Exception as e:
            print(e)
        finally:
            self.close_driver()


if __name__ == '__main__':
    start_time = time.clock()

    map_attraction_with_url = {}
    map_attraction_with_url.update({
        "Lake of the Restored Sword (Hoan Kiem Lake)":
        "https://www.tripadvisor.com/Attraction_Review-g293924-d311070-Reviews-Lake_of_the_Restored_Sword_Hoan_Kiem_Lake-Hanoi.html"
    })

    map_attraction_with_url.update({
        "Thap Rua Tower":
            "https://www.tripadvisor.com/Attraction_Review-g293924-d550756-Reviews-Thap_Rua_Tower-Hanoi.html"
    })

    map_attraction_with_url.update({
        "Cau The Huc":
        "https://www.tripadvisor.com/Attraction_Review-g293924-d11965985-Reviews-Cau_The_Huc-Hanoi.html"
    })

    map_attraction_with_url.update({
        "Post Office Ha Noi":
        "https://www.tripadvisor.com/Attraction_Review-g293924-d12231787-Reviews-Post_Office_Ha_Noi-Hanoi.html"
    })

    map_attraction_with_url.update({
        "Ly Thai To Park":
        "https://www.tripadvisor.com/Attraction_Review-g293924-d2067966-Reviews-Ly_Thai_To_Park-Hanoi.html"
    })


    map_attraction_with_url.update({
        "West Lake":
        "https://www.tripadvisor.com/Attraction_Review-g293924-d455016-Reviews-West_Lake-Hanoi.html"
    })

    map_attraction_with_url.update({
        "Truc Bach lake":
        "https://www.tripadvisor.com/Attraction_Review-g293924-d8300188-Reviews-Truc_Bach_lake-Hanoi.html"
    })

    map_attraction_with_url.update({
        "Chua Tran Quoc":
        "https://www.tripadvisor.com/Attraction_Review-g293924-d2067946-Reviews-Chua_Tran_Quoc-Hanoi.html"
    })

    map_attraction_with_url.update({
        "Quan Thanh Temple":
        "https://www.tripadvisor.com/Attraction_Review-g293924-d311081-Reviews-Quan_Thanh_Temple-Hanoi.html"
    })

    map_attraction_with_url.update({
        "Ho Tay Water Park":
        "https://www.tripadvisor.com/Attraction_Review-g293924-d2589683-Reviews-Ho_Tay_Water_Park-Hanoi.html"
    })

    map_attraction_with_url.update({
        "West Lake New Solar Amusement Park":
        "https://www.tripadvisor.com/Attraction_Review-g293924-d4317368-Reviews-West_Lake_New_Solar_Amusement_Park-Hanoi.html"
    })

    urlImageCrawler = URLImageCrawler()
    try:
        # map = urlImageCrawler.crawl_province("https://www.tripadvisor.com/Attractions-g293924-Activities-Hanoi.html")
        # urlImageCrawler.write_map(map, "./Data/VietNam/HaNoi_Attractions.txt")

        for attraction_name, url in map_attraction_with_url.items():
            url_images = urlImageCrawler.crawl_attraction(url)
            urlImageCrawler.write_url(url_images, "./Data/VietNam/HaNoi/{}.txt".format(attraction_name))
    finally:
        urlImageCrawler.close_driver()
        end_time = time.clock()
        print("[ * ] Time for executed CrawlURLImage (Trip advisor): {} seconds".format(end_time - start_time))