import os
from datetime import datetime

import pytz

TIME_ZONE = pytz.timezone('Asia/Dhaka')
NOW = datetime.now().astimezone(TIME_ZONE)
NOW_DATE = NOW.strftime('%Y-%m-%d')
NOW_DATE_TIME = NOW.strftime('%Y-%m-%d %H:%M:%S')
CHROMEDRIVER_PATH = 'chromedriver_linux64'

FB_MAIN_SITE = 'https://m.facebook.com/'
CHROME_HEADLESS = False
DIRNAME_POST_IMAGE = 'POST_IMAGE'
DIRNAME_ERROR_LOG = 'Error/'
DIRNAME_LAST = 'LAST/'
DIRNAME_REPORT = 'REPORT'
DIRNAME_SCRAPING_REPORT = 'SCRAPING'
DIRNAME_REPORT = 'REPORT'
DIRNAME_SCRAPING_REPORT = 'SCRAPING'
DIRNAME_FB_ERROR = f'{DIRNAME_REPORT}/{NOW_DATE}/{DIRNAME_SCRAPING_REPORT}/FACEBOOK_BLOCKING/'
TODAY = datetime.now().astimezone(TIME_ZONE).strftime('%Y-%m-%d')
file_path = f'{os.path.dirname(os.path.realpath(__file__))}/'