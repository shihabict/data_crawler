import time
from getpass import getpass

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# from scraping.web_scraping import DynamicScraper, FacebookScraper
from DATA.credentials import credential
from configs.fb_configs import DIRNAME_POST_IMAGE, TODAY, DIRNAME_SCRAPING_REPORT, DIRNAME_REPORT, FB_MAIN_SITE, \
    CHROME_HEADLESS, DIRNAME_FB_ERROR
from functions import make_dir_if_not_exists, get_driver, convert_fb_group_date_time, add_to_existing_json

# fb_groups_scraping = DynamicScraper(FB_GROUP_DIRNAME, FB_GROUPS_MAIN_SITE, FB_GROUPS_LOCAL_DB_COLUMNS)
# error_log = fb_groups_scraping.error_logger()
# fb_scraper = FacebookScraper()

# Image path
make_dir_if_not_exists(DIRNAME_POST_IMAGE)
make_dir_if_not_exists(DIRNAME_POST_IMAGE + '/' + TODAY)
image_path = f'{DIRNAME_POST_IMAGE}/'

# Path to save report_creation
report_path = f'{DIRNAME_REPORT}/{TODAY}/{DIRNAME_SCRAPING_REPORT}/'

job_links = []


# def scrap_fb_groups(driver, dir_error_data):
#     global SCRAPING_STATUS, last_scrap_date
#     last_scrap_date = fb_groups_scraping.read_last_scrape_moment()
#     id_exists_local_db = fb_groups_scraping.get_recent_jobs_id_fb_group()
#
#     total_existing_posts = 0  # Total existing posts counting
#     total_scraped_posts = 0  # Total scraped posts counting
#     id_exists_local_db_count = 0
#     total_posts_before_last_scrap = 0  # Total posts before last scrap counting
#     total_shared_posts = 0  # Total shared posts counting
#     total_saved_posts = 0  # Total Saved posts counting
#     total_existing_images = 0  # Total existing image counting
#     total_saved_images = 0  # Total Saved image counting
#
#     # driver = get_driver(FB_CREDENTIAL)
#
#     for fb_group in FB_GROUPS_AND_URLS:
#
#         scraped_posts = 0
#         posts_before_last_scrap = 0
#         saved_posts = 0
#         shared_posts = 0
#         existing_images = 0
#         saved_images = 0
#         existing_posts = 0
#         try:
#             # Added app running time
#             app_running_report = SaveRunnigTime(FB_GROUPS_AND_URLS[fb_group])
#             start = app_running_report.get_time()
#
#             print(f'Retrieving {FB_GROUPS_AND_URLS[fb_group]}-{fb_group}')
#
#             try:
#                 driver.get(fb_group)
#                 # m_fb_grpup_url = fb_group.replace('https://m.', 'https://m.')
#             except Exception as e:
#                 error_log.exception(e)
#                 print(f"Can't Retrieve {FB_GROUPS_AND_URLS[fb_group]}")
#                 fb_scraper.save_error_page(driver, fb_group, dir_error_data)
#                 app_status = Text().APP_RUNNING_STATUS_FAILED
#                 # continue
#
#             # Get all posts which are posted after the last scrap
#             check_fb_groups_last_scrap(driver, last_scrap_date)
#
#             posts = driver.find_elements_by_css_selector('section._7k7.storyStream._2v9s > article')
#
#             existing_posts = len(posts)
#             total_existing_posts += existing_posts
#             if posts:
#                 post_data = []
#
#                 # Get intended posts urls and post date
#                 for post in posts:
#                     try:
#                         # Check shared post
#                         try:
#                             posted_info = post.find_element_by_css_selector('header h3').text
#                         except Exception as e:
#                             error_log.exception(e)
#                         if 'shared a post' in posted_info:
#                             shared_posts += 1
#                             continue
#
#                         # Get post date
#                         try:
#                             post_date_txt = post.find_element_by_css_selector(
#                                 '._52jc._5qc4._78cz._24u0._36xo abbr').text
#                         except:
#                             post_date_txt = post.find_element_by_css_selector('._52jc._5qc4._78cz._24u0._9s6 abbr').text
#                         try:
#                             post_date = convert_fb_group_date_time(post_date_txt)
#
#                         except Exception as e:
#                             error_log.exception(e)
#
#                         # Get post URL
#                         all_url = post.find_elements_by_css_selector('._5rgt._5nk5._5msi a')
#                         for url in all_url:
#                             url = url.get_attribute('href')[:88]
#                             try:
#                                 if ".com/story.php?" in url or ".com/groups" in url:
#                                     post_url = url
#                                     break
#                             except Exception as e:
#                                 error_log.exception(e)
#
#                         # Checking existence
#                         if post_url in job_links:
#                             continue
#
#                         # Checking post date
#                         if post_date:
#                             if post_date < last_scrap_date:
#                                 posts_before_last_scrap += 1
#                                 continue
#
#                         job_links.append(url)
#
#                         # Check image existence
#                         if 'shared a link' not in posted_info:
#                             try:
#                                 img_container = post.find_element_by_css_selector('._5rgu._7dc9._27x0')
#                                 img = img_container.find_elements_by_css_selector('a')
#                                 has_image = len(img)
#                                 existing_images += has_image
#                             except NoSuchElementException:
#                                 has_image = False
#                         else:
#                             has_image = False
#
#                         post_data.append({
#                             "has_image": has_image,
#                             "post_date": post_date,
#                             "job_url_1": post_url,
#                             "job_source_1_id": FB_GROUPS_AND_URLS[fb_group]
#                         })
#                     except Exception as e:
#                         print(e)
#                 # Get content from each post
#                 for post in post_data:
#                     post_id = extract_id_from_url(post['job_url_1'])
#                     if post_id in id_exists_local_db:
#                         id_exists_local_db_count += 1
#                         print("This ID is already exists in local DB")
#                         continue
#                     try:
#                         # Get content from m.facebook
#                         # Go to full post
#                         driver.get(post['job_url_1'])
#                         time.sleep(5)
#
#                         # Get raw content
#                         try:
#                             post['raw_content'] = driver.find_element_by_css_selector('._5rgt._5nk5').get_attribute(
#                                 'innerHTML')
#                         except Exception as e:
#                             error_log.exception(e)
#
#                         scraped_posts += 1
#
#                         if post['has_image']:
#
#                             # Get image URL
#                             if post['has_image'] == 1:
#                                 img_url = driver.find_element_by_css_selector('a._39pi').get_attribute('href')
#                                 img_url = img_url.replace('https://m.', 'https://m.')
#                                 driver.get(img_url)
#                                 time.sleep(5)
#
#                                 try:
#                                     WebDriverWait(driver, 20).until(EC.presence_of_element_located(
#                                         (By.CSS_SELECTOR, 'img.gitj76qy.r9f5tntg.d2edcug0')))
#                                     img_url = driver.find_element_by_css_selector(
#                                         'img.gitj76qy.r9f5tntg.d2edcug0').get_attribute('src')
#                                 except Exception as e:
#                                     error_log.exception(e)
#                                     try:
#                                         WebDriverWait(driver, 20).until(EC.presence_of_element_located(
#                                             (By.CSS_SELECTOR, '.bp9cbjyn.j83agx80.l9j0dhe7.pw8zj2ei.bkyfam09 img')))
#                                         img_url = driver.find_element_by_css_selector(
#                                             '.bp9cbjyn.j83agx80.l9j0dhe7.pw8zj2ei.bkyfam09 img').get_attribute('src')
#                                     except Exception as e:
#                                         error_log.exception(e)
#                                         try:
#                                             WebDriverWait(driver, 20).until(EC.presence_of_element_located((
#                                                                                                            By.CSS_SELECTOR,
#                                                                                                            '.iqfcb0g7.kr520xx4.j9ispegn.pmk7jnqg.akz8cqyu.n7fi1qx3.i09qtzwb img')))
#                                             img_url = driver.find_element_by_css_selector(
#                                                 '.iqfcb0g7.kr520xx4.j9ispegn.pmk7jnqg.akz8cqyu.n7fi1qx3.i09qtzwb img').get_attribute(
#                                                 'src')
#                                         except Exception as e:
#                                             error_log.exception(e)
#
#                             try:
#                                 image_downloader(img_url, post['job_url_1'], image_path)
#                                 saved_images += 1
#                             except Exception as e:
#                                 error_log.exception(e)
#                                 save_report(post['job_url_1'], 'Not saved Image URL', image_path)
#
#                         # Save to localhost
#                         try:
#                             saved_posts = fb_groups_scraping.save_to_local_db(post, saved_posts)
#                         except Exception as e:
#                             error_log.exception(e)
#                     except Exception as e:
#                         error_log.exception(e)
#
#                 app_status = Text().APP_RUNNING_STATUS_SUCCESS
#             else:
#                 fb_scraper.save_error_page(driver, fb_group, dir_error_data)
#                 print("No content available or something else")
#                 app_status = Text().APP_RUNNING_STATUS_FAILED
#                 time.sleep(3)
#                 # continue
#
#             time.sleep(3)
#
#             # Group Report
#             report = {
#                 'Source name': FB_GROUPS_AND_URLS[fb_group],
#                 'Existing Posts': existing_posts,
#                 'Shared Posts': shared_posts,
#                 'Before last scrap Posts': posts_before_last_scrap,
#                 'Scraped Posts': scraped_posts,
#                 'Saved Posts': saved_posts,
#                 'Existing images': existing_images,
#                 'Saved images': saved_images
#             }
#             save_and_show_report(report, FB_GROUP_DIRNAME, report_path)
#             save_updated_existing_summary_report({FB_GROUPS_AND_URLS[fb_group]: saved_posts},
#                                                  FILE_NAME_REPORT_SCRAPING_SUMMARY, report_path)
#
#             total_scraped_posts += scraped_posts
#             total_posts_before_last_scrap += posts_before_last_scrap
#             total_shared_posts += shared_posts
#             total_saved_posts += saved_posts
#             total_existing_images += existing_images
#             total_saved_images += saved_images
#
#             # End the scraping for a group
#             end = app_running_report.get_time()
#             app_running_report.save_start_end_time(start, end, app_status)
#         except Exception as e:
#             error_log.exception(e)
#
#     # Total Report
#     report = {
#         'Facebook Group': 'Total Report',
#         'Existing Posts': total_existing_posts + id_exists_local_db_count,
#         'Shared Posts': total_shared_posts,
#         'Before last scrap Posts': total_posts_before_last_scrap,
#         'Scraped Posts': total_scraped_posts,
#         'Saved Posts': total_saved_posts,
#         'Existing images': total_existing_images,
#         'Saved images': total_saved_images
#     }
#     save_and_show_report(report, FB_GROUP_DIRNAME, report_path)
#     save_updated_existing_summary_report({'Facebook Groups Total': total_saved_posts},
#                                          FILE_NAME_REPORT_SCRAPING_SUMMARY, report_path)
#
#     # Save scrap time
#     fb_groups_scraping.write_last_scrap_moment()
#     print(f'{id_exists_local_db_count} ID exists in local DB')
#     print('Successfully completed!')


class FacebookScraper():

    def __init__(self, driver):
        self.driver = driver

    def is_blocked(self, driver):
        block_text = driver.find_element_by_css_selector('div._e6s span').text
        if block_text == 'Sorry, something went wrong.':
            return True

    def save_error_page(self, driver, url, dir_error_data):
        url = url.replace('/', '_')
        img_path = f'{dir_error_data}{url}.png'
        driver.save_screenshot(img_path)
        content = driver.page_source
        with open(f'{dir_error_data}{url}.html', 'w') as f:
            f.write(content)
        data_dict = {
            'URL': url
        }
        # send_blocking_status(data_dict, img_path)

    # Request to URL using Chrome driver
    def fb_login(self, driver, url, fb_credential, dir_error_data):

        try:
            driver.find_element_by_name('email').send_keys(fb_credential['Email'])
            driver.find_element_by_name('pass').send_keys(fb_credential['Password'])
            driver.find_element_by_name('login').click()
            driver.implicitly_wait(5)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                            "#root > div._7om2 > div > div > div._7om2._2pip > div:nth-child(1) > div > div > a"))).click()

        except:
            self.save_error_page(driver, url, dir_error_data)
            input('solve the blocking issue & give 1 : ')
        return driver

    def get_comments(self, post_dict,exist):
        comments = post_dict['comment']
        comment_list = []
        try:
            post_comments = self.driver.find_elements_by_css_selector('._2b06 > div:nth-child(2)')[exist:]
            time.sleep(3)
            # # post_comments = self.driver.find_elements_by_xpath('//*[@id="5373587219319405"]/div[2]')
            i = 0

            for post in post_comments:
                # time.sleep(2)
                i += 1
                if post.text not in comments:
                    comment_list.append(post.text)
                # post_dict[f"comment"] = post.text
        except Exception as e:
            print(e)
        post_dict['comment'] = comments + comment_list
        return post_dict

    def get_post_comments(self, post_dict):
        post_dict['comment'] = []
        MORE_COMMENT = True
        exist = 0
        comment_length = 0
        try:
            # while MORE_COMMENT:
            try:
                while True:
                    # i += 1
                    try:
                        # see_more = self.driver.find_element_by_id('see_next_841423427253651')
                        # see_more = self.driver.find_element_by_id('see_next_10160644725444644')
                        # see_more = self.driver.find_element_by_css_selector('.async_elem a')
                        see_more = self.driver.find_element_by_css_selector('._108_')
                        time.sleep(2)
                    except:
                        # see_more = self.driver.find_element_by_id('see_next_3433306610113400')
                        see_more = self.driver.find_element_by_id('see_next_4799402573503790')

                    if see_more:
                        # time.sleep(3)
                        # see_more.click()
                        # time.sleep(3)
                        SCROLL_PAUSE_TIME = 3

                        # Get scroll height
                        last_height = self.driver.execute_script("return document.body.scrollHeight")
                        see_more.click()
                        time.sleep(3)
                        comments = self.driver.find_elements_by_css_selector('._2b04')[comment_length:]
                        comment_length+=len(comments)
                        if comments:
                            for comment in comments:
                                if comment.text[-4:] != 'More':
                                    try:
                                        post_reply = comment.find_element_by_css_selector('._2b1h.async_elem')
                                        if post_reply:
                                            time.sleep(2)
                                            post_reply.click()
                                    except Exception as e:
                                        print(e)
                            post_dict = self.get_comments(post_dict, exist)
                            exist =+ len(post_dict['comment'])
                        # Scroll down to bottom
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        # Wait to load page
                        time.sleep(SCROLL_PAUSE_TIME)

                        # Calculate new scroll height and compare with last scroll height
                        new_height = self.driver.execute_script("return document.body.scrollHeight")

                        if new_height == last_height:
                            break
                        last_height = new_height
                    else:
                        MORE_COMMENT = False
            except Exception as e:
                print(e)

            # comments = self.driver.find_elements_by_css_selector('._2b04')
            # if comments:
            #     for comment in comments:
            #         if comment.text[-4:] != 'More':
            #             post_reply = comment.find_element_by_css_selector('._2b1h.async_elem')
            #             if post_reply:
            #                 time.sleep(2)
            #                 post_reply.click()
            #     post_dict = self.get_comments(post_dict)
        except Exception as e:
            print(e)
        return post_dict

    def scrap_post_data(self, POST_LINKS):
        file_dir = f"DATA/comments_3.json"
        for post in POST_LINKS:
            post_dict = {}
            post_dict['url'] = post
            self.driver.get(post)
            time.sleep(3)
            print("INTO POST")
            # Get post date
            # try:
            #     post_date_txt = self.driver.find_element_by_css_selector(
            #         '._52jc._5qc4._78cz._24u0._36xo abbr').text
            # except:
            #     post_date_txt = self.driver.find_element_by_css_selector('._52jc._5qc4._78cz._24u0._9s6 abbr').text
            # try:
            #     post_date = convert_fb_group_date_time(post_date_txt)
            #
            # except Exception as e:
            #     print(e)
            #     # error_log.exception(e)
            # post_dict['post_date'] = post_date_txt
            # # Get raw content
            # try:
            #     post_dict['raw_content'] = self.driver.find_element_by_css_selector('._5rgt._5nk5').get_attribute(
            #         'innerHTML')
            # except Exception as e:
            #     print(e)
            # # error_log.exception(e)
            # time.sleep(2)
            try:
                post_dict = self.get_post_comments(post_dict)
            except Exception as e:
                print(e)

            try:
                add_to_existing_json(post_dict, file_dir)
            except Exception as e:
                print(e)


if __name__ == '__main__':

    fb_credential = credential
    POST_LINKS = [
        # 'https://m.facebook.com/story.php?story_fbid=10160644725444644&id=13678589643&fs=60&focus_composer=0&m_entstream_source=video_home&player_suborigin=entry_point&player_format=permalink']

        # 'https://m.facebook.com/story.php?story_fbid=4799402573503790&id=530522153725208&fs=60&focus_composer=0&m_entstream_source=video_home&player_suborigin=entry_point&player_format=permalink']

        # 'https://m.facebook.com/story.php?story_fbid=4457061927737858&id=530522153725208&fs=60&focus_composer=0&m_entstream_source=video_home&player_suborigin=entry_point&player_format=permalink']

        # 'https://m.facebook.com/story.php?story_fbid=4514545591989491&id=530522153725208&fs=60&focus_composer=0&m_entstream_source=video_home&player_suborigin=entry_point&player_format=permalink']
        # 'https://m.facebook.com/independent24Television/photos/a.145312182227935/3482992568459863'
        # 'https://m.facebook.com/independent24Television/posts/1978309182261550'
        # 'https://m.facebook.com/independent24Television/posts/4009261712499610'
        # 'https://m.facebook.com/independent24Television/posts/4078754722216975'
        # 'https://m.facebook.com/story.php?story_fbid=260255265513662&id=530522153725208&fs=60&focus_composer=0&m_entstream_source=video_home&player_suborigin=entry_point&player_format=permalink'
        # 'https://m.facebook.com/story.php?story_fbid=260255265513662&id=530522153725208&fs=60&focus_composer=0&m_entstream_source=video_home&player_suborigin=entry_point&player_format=permalink'
        # 'https://m.facebook.com/story.php?story_fbid=4224548064322580&id=530522153725208&fs=60&focus_composer=0&m_entstream_source=video_home&player_suborigin=entry_point&player_format=permalink'
        # 'https://m.facebook.com/story.php?story_fbid=4457061927737858&id=530522153725208&fs=60&focus_composer=0&m_entstream_source=video_home&player_suborigin=entry_point&player_format=permalink'
    ]

    # POST_LINKS = [
    #     'https://m.facebook.com/story.php?story_fbid=4224548064322580&id=530522153725208&fs=60&focus_composer=0&m_entstream_source=video_home&player_suborigin=entry_point&player_format=permalink',
    #
    #     'https://m.facebook.com/story.php?story_fbid=4457061927737858&id=530522153725208&fs=60&focus_composer=0&m_entstream_source=video_home&player_suborigin=entry_point&player_format=permalink',

    #     'https://m.facebook.com/story.php?story_fbid=3177320062378724&id=530522153725208&fs=60&focus_composer=0&m_entstream_source=video_home&player_suborigin=entry_point&player_format=permalink']

    # Scrape from facebook
    make_dir_if_not_exists(DIRNAME_FB_ERROR)
    driver = get_driver(FB_MAIN_SITE, headless=CHROME_HEADLESS)
    fb_driver = FacebookScraper(driver)
    fb_driver.fb_login(driver, FB_MAIN_SITE, fb_credential, DIRNAME_FB_ERROR)
    fb_driver.scrap_post_data(POST_LINKS)

    # fb_driver = FacebookScraper().fb_login(FB_MAIN_SITE, fb_credential)
    # scrap_fb_groups(fb_driver)
    # fb_driver.quit()
