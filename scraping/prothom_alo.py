import json
import time

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from settings import BASE_DIR, NUM_PAGES
from scraping.helpers import get_driver, add_to_existing_json


class ProthomAloScrapper:
    def __init__(self, driver):
        self.driver = driver

    def scroll_to_element(self, driver, el: WebElement):
        driver.execute_script("arguments[0].scrollIntoView(true);", el)
        time.sleep(3)

    def get_cat_urls(self):
        category_dict = {}
        categories = self.driver.find_elements_by_css_selector('li.menu-item')
        for category in categories:
            category_dict[category.text] = category.find_element_by_css_selector('div a').get_attribute('href')
        return category_dict

    def get_post_urls(self, driver, exist):
        post_dict = {}
        # post_urls = self.driver.find_elements(By.CSS_SELECTOR, value='.headline-title.newsHeadline-m__title__2_I3j')[exist:]
        try:
            post_urls = self.driver.find_elements_by_css_selector('.headline-title.newsHeadline-m__title__2_I3j')[
                        exist:]
            # post_urls = driver.find_elements_by_css_selector('.newsHeadline-m__title-link__1puEG')[exist:]
        except Exception as e:
            print(e)
        for post in post_urls:
            try:
                post_dict[post.text] = post.find_element_by_css_selector('a').get_attribute('href')
            except Exception as e:
                print(e)
        return post_dict

    def get_sub_cat_urls(self):
        category_dict = {}
        categories = self.driver.find_elements_by_css_selector('li.section-m__section__1cztQ')
        for category in categories:
            category_dict[category.text] = category.find_element_by_css_selector('a').get_attribute('href')
        return category_dict

    def get_posts(self, category, category_name, post_urls, existing, data_file):
        # driver = self.driver
        if category:
            i = 1
            try:

                # SCRAPING_STATUS = True
                print(f"No of post URLS: {len(post_urls)}")
                for url in post_urls:
                    print("*******************************************************************************")
                    post_url = post_urls[url]
                    print(f"POST URL: {post_url}")
                    # for url in post_urls:
                    saved = 0
                    if post_url not in existing:
                        data_dict = {'title': url, 'category': category_name}

                        # time.sleep(2)
                        self.driver.execute_script(f"window.open('{post_url}', 'new_window')")
                        time.sleep(2)
                        self.driver.switch_to.window(self.driver.window_handles[1])
                        time.sleep(2)
                        try:
                            data_dict['url'] = self.driver.current_url
                        except Exception as e:
                            print(e)
                            data_dict['url'] = post_url
                        try:
                            data_dict['published_date'] = self.driver.find_element_by_class_name(
                                'storyPageMetaData-m__publish-time__19bdV').text
                            # time.sleep(2)
                        except Exception as e:
                            print(e)

                        try:
                            # time.sleep(2)
                            # paragraphs = driver.find_elements_by_class_name('story-element.story-element-text')
                            paragraphs = self.driver.find_elements_by_css_selector(
                                'div.story-element.story-element-text')
                            text = ''
                            for paragraph in paragraphs:
                                text += f'{paragraph.get_attribute("innerText")}\n\n'
                            data_dict['raw_text'] = text
                            # time.sleep(2)
                        except Exception as e:
                            print(e)

                        try:
                            add_to_existing_json(data_dict, data_file)
                            i += 1
                            print(f"Saved :{i}")
                        except Exception as e:
                            print(e)

                        # Switch to the tab
                        time.sleep(4)
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        time.sleep(2)
                    else:
                        print('URL Already Exist')
            except Exception as e:
                print(e)
        # except Exception as e:
        #     print(e)

    def main_prothom_alo(self):
        categories = scraper.get_cat_urls()
        special_cat = ["সর্বশেষ", 'বিশেষ সংবাদ', 'রাজনীতি', 'করোনাভাইরাস', 'বাংলাদেশ', 'বিশ্ব', 'বাণিজ্য', 'মতামত']
        SCRAPING_STATUS = True
        for cat in categories:
            time.sleep(10)
            if cat not in special_cat:
                print(cat)
                data_file = f'{BASE_DIR}/DATASET/prothomalo_{cat}.json'

                try:
                    with open(data_file, "r") as the_file:
                        existing = json.load(the_file)
                    existing = [data['url'] for data in existing]
                except:
                    existing = []

                print(f"Existing URLS: {len(existing)}")
                time.sleep(10)
                print(categories[cat])
                self.driver.get(categories[cat])
                exist = 0
                while SCRAPING_STATUS:
                    # pass
                    try:
                        urls_list = []
                        if exist == 0:
                            post_urls = self.get_post_urls(exist)
                        exist += len(post_urls)
                        scraper.get_posts(categories[cat], cat, post_urls, existing, data_file)

                        # load more
                        try:
                            time.sleep(2)
                            load_more = self.driver.find_element_by_css_selector('.load-more-content')
                            self.scroll_to_element(self.driver, load_more)

                            javascript = "document.querySelector('.load-more-content').click();"
                            self.driver.execute_script(javascript)
                            time.sleep(4)
                        except Exception as e:
                            print(e)
                        post_urls = self.get_post_urls(exist)
                        print(0)

                    except Exception as e:
                        print(e)
                        SCRAPING_STATUS = False
                        break
        print(0)

    def scrap_based_urls(self):
        SCRAPING_STATUS = True
        categories = {"বিশ্ব": "https://www.prothomalo.com/world",
                      "লাইফস্টাইল": "https://www.prothomalo.com/lifestyle",
                      "বাংলাদেশ": "https://www.prothomalo.com/bangladesh",
                      "রাজনীতি": "https://www.prothomalo.com/politics",
                      "বিশ্ববাণিজ্য": "https://www.prothomalo.com/business/world-business",
                      "চাকরি": "https://www.prothomalo.com/chakri"}

        for cat in categories:
            data_file = f'{BASE_DIR}\DATASET_2\prothomalo_{cat}.json'

            try:
                with open(data_file, "r", encoding="utf8") as the_file:
                    try:
                        existing = json.load(the_file)
                    except Exception as e:
                        print(e)
                existing = [data['url'] for data in existing]
            except:
                existing = []

            print(f"Existing URLS: {len(existing)}")
            print(categories[cat])
            self.driver.get(categories[cat])
            exist = 0
            while SCRAPING_STATUS:
                driver = self.driver
                # pass
                try:
                    urls_list = []
                    if exist == 0:
                        post_urls = self.get_post_urls(driver, exist)
                    exist += len(post_urls)
                    scraper.get_posts(categories[cat], cat, post_urls, existing, data_file)
                    # scraper.get_posts(cat, cat_name, existing, data_file)
                    # load more
                    try:
                        time.sleep(2)
                        load_more = self.driver.find_element_by_css_selector('.load-more-content')
                        self.scroll_to_element(self.driver, load_more)

                        javascript = "document.querySelector('.load-more-content').click();"
                        self.driver.execute_script(javascript)
                        time.sleep(2)
                    except Exception as e:
                        print(e)
                    post_urls = self.get_post_urls(driver, exist)
                    print(0)

                except Exception as e:
                    print(e)
                    SCRAPING_STATUS = False
                    break


if __name__ == "__main__":
    chrome_version = chromedriver_autoinstaller.get_chrome_version()
    driver_dcra = get_driver('https://www.prothomalo.com/', chrome_version=chrome_version, headless=False)
    scraper = ProthomAloScrapper(driver_dcra)
    # scraper.main_prothom_alo()
    scraper.scrap_based_urls()
