import json
import os
import shutil
import time
import re
import simplejson
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException
from get_chrome_driver import GetChromeDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


# Request to URL using Chrome driver
from configs.fb_configs import CHROMEDRIVER_PATH


def get_driver(url, headless=True):
    option = Options()
    option.add_argument("--disable-notifications")
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')

    if headless:
        option.add_argument("--headless")

    chrome_dir = os.path.dirname(os.path.realpath(__file__))+'/'+CHROMEDRIVER_PATH
    make_dir_if_not_exists(chrome_dir)
    chrome_file_path = chrome_dir + '/chromedriver'

    try:
        driver = webdriver.Chrome(chrome_file_path, chrome_options=option)
        driver.get(url)
    except Exception as e:
        print('Selenium session is not Created !')

        if os.path.exists(chrome_file_path):
            os.remove(chrome_file_path)
            print(f'Removed {chrome_file_path} file!')

        download_driver = GetChromeDriver()
        download_driver.auto_download(extract=True, output_path=chrome_dir)
        print(f'Downloaded chrome driver for the chrome version {download_driver.matching_version()}!')
        driver = webdriver.Chrome(chrome_file_path, chrome_options=option)
        driver.get(url)

    driver.maximize_window()
    return driver


# Convert date time of facebook group
def convert_fb_group_date_time(date_time):
    now = datetime.now()
    if date_time == 'Now' or date_time == 'Just now':
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    elif 'min' in date_time:
        mins = int("".join(filter(str.isdigit, date_time)))
        date_time = now - timedelta(minutes=mins)
        date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
    elif 'hr' in date_time:
        hrs = int("".join(filter(str.isdigit, date_time)))
        date_time = now - timedelta(hours=hrs)
        date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
    elif 'Today' in date_time:
        date = datetime.strftime(now, '%Y-%m-%d')
        time_split = date_time.split(' at ')[1]
        time_split = datetime.strptime(time_split, '%H:%M').strftime("%H:%M:%S")
        date_time = str(date) + ' ' + str(time_split)
    elif 'Yesterday' in date_time:
        date = datetime.strftime(now - timedelta(days=1), '%Y-%m-%d')
        time_split = date_time.split(' at ')[1]
        try:
            c_f = datetime.strptime(time_split, '%I:%M %p')
        except:
            c_f = datetime.strptime(time_split, '%H:%M')
        time_split = datetime.strftime(c_f, '%H:%M:%S')
        date_time = date + ' ' + time_split
    else:
        try:
            try:
                date_time = datetime.strptime(date_time, '%B %d at %I:%M %p')
            except:
                try:
                    date_time = time.strptime(date_time, '%B %d at %I:%M %p')
                    date_time = datetime(int(now.strftime("%Y")), date_time.tm_mon, date_time.tm_mday,
                                         date_time.tm_hour, date_time.tm_min, date_time.tm_sec)
                except:
                    try:
                        date_time = datetime.strptime(date_time, '%d %B at %H:%M')
                    except:
                        try:
                            date_time = datetime.strptime(date_time, '%d %B at %I:%M')
                        except:
                            try:
                                date_time = datetime.strptime(date_time, '%d %B %Y at %I:%M')
                            except:
                                date_time = datetime.strptime(date_time, '%d %B %Y at %H:%M')

            this_year = datetime.strftime(now, '%Y')
            if '1900' in str(date_time):
                date_time = str(date_time).replace("1900", this_year)
                date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            date_time = datetime.strptime(date_time, '%B %d, %Y at %I:%M %p')

    date_time = datetime.strptime(str(date_time), '%Y-%m-%d %H:%M:%S')
    return date_time

# Scroll to element
def scroll_to_element(driver, el: WebElement):
    driver.execute_script("arguments[0].scrollIntoView(true);", el)
    time.sleep(3)

# check directory if not exists then make directory
def make_dir_if_not_exists(file_path):
    dirs = file_path.split('/')
    if dirs:
        path = ''
        for dir in dirs:
            if dir:
                path = path + dir + '/'
                if not os.path.exists(path):
                    os.mkdir(path)

# remove file if exists
def remove_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f'{file_path} file successfully removed!')
    else:
        print(f'{file_path} path not exists!')


# remove dir if exists
def remove_dir_if_exists(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print(f'{dir_path} directory successfully removed!')
    else:
        print(f'{dir_path} path not exists!')

def convert_datetime_to_str(o):
    if isinstance(o, datetime):
        return o.__str__()
    if isinstance(o, date):
        return o.__str__()

def add_to_existing_json(data, file):
    dirs = file.split('/')

    try:
        if len(dirs)>=2:
            dir = dirs[:-1]
            make_dir_if_not_exists('/'.join(dir))
    except Exception as e:
        print(e)

    try:
        with open(file, "r") as the_file:
            existing = json.load(the_file)
    except FileNotFoundError as e:
        print(e)
        existing = []
    existing.append(data)

    with open(file, "w") as the_file:
        simplejson.dump(existing, the_file, indent=4, default = convert_datetime_to_str)

    print(f'Saved to {file}')