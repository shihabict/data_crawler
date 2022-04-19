import json
import time

import chromedriver_autoinstaller
from selenium.webdriver.remote.webelement import WebElement

from scraping.helpers import get_driver, add_to_existing_json
from settings import BASE_DIR


class JagoNews24:
    def __init__(self,driver):
        self.driver = driver

    def get_post_urls(self,driver, exist):
        post_dict = {}
        try:
            post_urls = self.driver.find_elements_by_css_selector('.tag-block h3 a')[exist:]
        except Exception as e:
            print(e)
        for post in post_urls:
            try:
                # post_dict[post.text] = post.find_element_by_css_selector('a').get_attribute('href')
                # print(post.text)
                # print(post.get_attribute('href'))
                post_dict[post.text] = post.get_attribute('href')
            except Exception as e:
                print(e)
        return post_dict

    def get_post_urls_politics(self,driver,exist):
        post_dict = {}
        try:
            post_urls = self.driver.find_elements_by_css_selector('.single-block.cat-block h3 a')[exist:]
        except Exception as e:
            print(e)
        for post in post_urls:
            try:
                # post_dict[post.text] = post.find_element_by_css_selector('a').get_attribute('href')
                # print(post.text)
                # print(post.get_attribute('href'))
                post_dict[post.text] = post.get_attribute('href')
            except Exception as e:
                print(e)
        return post_dict

    def scroll_to_element(self, driver, el: WebElement):
        driver.execute_script("arguments[0].scrollIntoView(true);", el)
        time.sleep(3)

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

                        time.sleep(2)
                        self.driver.execute_script(f"window.open('{post_url}', 'new_window')")
                        time.sleep(2)
                        self.driver.switch_to.window(self.driver.window_handles[1])
                        time.sleep(2)
                        try:
                            data_dict['url'] = self.driver.current_url
                        except Exception as e:
                            data_dict['url'] = post_url
                        # try:
                        #     data_dict['published_date'] = self.driver.find_element_by_class_name(
                        #         '.time-with-author').text
                        #     time.sleep(2)
                        # except Exception as e:
                        #     print(e)

                        try:
                            # time.sleep(2)
                            # paragraphs = driver.find_elements_by_class_name('story-element.story-element-text')
                            paragraphs = self.driver.find_elements_by_css_selector(
                                '.content-details p')
                            text = ''
                            for paragraph in paragraphs[:-1]:
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
                        time.sleep(2)
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        time.sleep(2)
                    else:
                        print('URL Already Exist')
            except Exception as e:
                print(e)

    def get_posts_politics(self, category, category_name, post_urls, existing, data_file):
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

                        time.sleep(2)
                        self.driver.execute_script(f"window.open('{post_url}', 'new_window')")
                        time.sleep(2)
                        self.driver.switch_to.window(self.driver.window_handles[1])
                        time.sleep(2)
                        try:
                            data_dict['url'] = self.driver.current_url
                        except Exception as e:
                            data_dict['url'] = post_url
                        # try:
                        #     data_dict['published_date'] = self.driver.find_element_by_class_name(
                        #         '.time-with-author').text
                        #     time.sleep(2)
                        # except Exception as e:
                        #     print(e)

                        try:
                            # time.sleep(2)
                            # paragraphs = driver.find_elements_by_class_name('story-element.story-element-text')
                            paragraphs = self.driver.find_elements_by_css_selector(
                                '.content-details p')
                            text = ''
                            for paragraph in paragraphs[:-1]:
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
                        time.sleep(2)
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        time.sleep(2)
                    else:
                        print('URL Already Exist')
            except Exception as e:
                print(e)


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

                        time.sleep(2)
                        self.driver.execute_script(f"window.open('{post_url}', 'new_window')")
                        time.sleep(2)
                        self.driver.switch_to.window(self.driver.window_handles[1])
                        time.sleep(2)
                        try:
                            data_dict['url'] = self.driver.current_url
                        except Exception as e:
                            data_dict['url'] = post_url
                        # try:
                        #     data_dict['published_date'] = self.driver.find_element_by_class_name(
                        #         '.time-with-author').text
                        #     time.sleep(2)
                        # except Exception as e:
                        #     print(e)

                        try:
                            # time.sleep(2)
                            # paragraphs = driver.find_elements_by_class_name('story-element.story-element-text')
                            paragraphs = self.driver.find_elements_by_css_selector(
                                '.content-details p')
                            text = ''
                            for paragraph in paragraphs[:-1]:
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
                        time.sleep(2)
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        time.sleep(2)
                    else:
                        print('URL Already Exist')
            except Exception as e:
                print(e)

    def scrap_jagonews(self):
        especial_cat = ["আন্তর্জাতিক","রাজনীতি"]
        SCRAPING_STATUS = True
        categories = {"আন্তর্জাতিক":"https://www.jagonews24.com/international","শিক্ষা":"https://www.jagonews24.com/education","রাজনীতি":"https://www.jagonews24.com/politics","চাকরি":"https://www.jagonews24.com/topic/%E0%A6%9A%E0%A6%BE%E0%A6%95%E0%A6%B0%E0%A6%BF%E0%A6%B0-%E0%A6%96%E0%A6%AC%E0%A6%B0?utm_source=jagonews_trending","করোনাভাইরাস": "https://www.jagonews24.com/topic/%E0%A6%95%E0%A6%B0%E0%A7%8B%E0%A6%A8%E0%A6%BE%E0%A6%AD%E0%A6%BE%E0%A6%87%E0%A6%B0%E0%A6%BE%E0%A6%B8"}

        for cat in categories:
            data_file = f'{BASE_DIR}\DATASET_2\jagonews_{cat}.json'

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
                if cat in especial_cat:
                    try:
                        urls_list = []
                        if exist == 0:
                            post_urls = self.get_post_urls_politics(self.driver, exist)
                        exist += len(post_urls) - 1
                        scraper.get_posts_politics(categories[cat], cat, post_urls, existing, data_file)
                        # scraper.get_posts(cat, cat_name, existing, data_file)
                        # load more
                        try:
                            time.sleep(2)
                            load_more = self.driver.find_element_by_css_selector('#load_more_button')
                            self.scroll_to_element(self.driver, load_more)

                            javascript = "document.querySelector('#load_more_button').click();"
                            self.driver.execute_script(javascript)
                            time.sleep(2)
                        except Exception as e:
                            print(e)
                        print(f"Scapped : {exist}")
                        post_urls = self.get_post_urls_politics(self.driver, exist)
                        print(0)

                    except Exception as e:
                        print(e)
                        SCRAPING_STATUS = False
                        break
                else:
                    try:
                        urls_list = []
                        if exist == 0:
                            post_urls = self.get_post_urls(self.driver,exist)
                        exist += len(post_urls)-1
                        scraper.get_posts(categories[cat], cat, post_urls, existing, data_file)
                        # scraper.get_posts(cat, cat_name, existing, data_file)
                        # load more
                        try:
                            time.sleep(2)
                            load_more = self.driver.find_element_by_css_selector('#load_more_button')
                            self.scroll_to_element(self.driver, load_more)

                            javascript = "document.querySelector('#load_more_button').click();"
                            self.driver.execute_script(javascript)
                            time.sleep(2)
                        except Exception as e:
                            print(e)
                        post_urls = self.get_post_urls(self.driver,exist)
                        print(0)

                    except Exception as e:
                        print(e)
                        SCRAPING_STATUS = False
                        break


if __name__ == "__main__":
    chrome_version = chromedriver_autoinstaller.get_chrome_version()
    driver_dcra = get_driver('https://www.jagonews24.com/', chrome_version=chrome_version, headless=False)
    scraper = JagoNews24(driver_dcra)
    scraper.scrap_jagonews()
