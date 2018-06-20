import platform
import pprint
import time
from random import shuffle

import feedparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def display_codepen(driver, entry):
    pprint.pprint(entry)
    entry_fullscreen_url = entry['link'].replace('/pen/', '/full/')
    print(entry_fullscreen_url)
    driver.get(entry_fullscreen_url)


def display_nasa_image(driver, entry):
    pprint.pprint(entry)
    image_url = list(filter(lambda l: l['rel'] == 'enclosure', entry['links']))[0]['href']
    driver.get(image_url)


def display_flikr_image(driver, entry):
    pprint.pprint(entry)
    image_url = list(filter(lambda l: l['rel'] == 'enclosure', entry['links']))[0]['href']
    driver.get(image_url)


def get_driver():
    os_name = platform.system()
    print(os_name)
    is_linux = os_name == "Linux"
    is_mac = os_name == "Darwin"
    is_windows = os_name == "Windows"
    chrome_options = Options()
    chrome_options.add_argument('--kiosk')  # fullscreen
    # failed attempt to remove the warning message
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--test-type')
    if is_linux:
        executable_path = '/usr/lib/chromium-browser/chromedriver'
        driver = webdriver.Chrome(
            executable_path=executable_path,
            chrome_options=chrome_options
        )
    elif is_windows or is_mac:
        driver = webdriver.Chrome(
            chrome_options=chrome_options
        )
    else:
        raise Exception(os_name)
    return driver


class FeedItem(object):
    def __init__(self, url, display_func):
        self.url = url
        self.display_func = display_func

    def get_entries(self):
        # print(url)
        feed = feedparser.parse(self.url)
        # pprint.pprint(feed)
        # print(len(feed.entries))

        return list(map(self.get_entry, feed.entries))

    def get_entry(self, e):
        return EntryItem(e, self.display_func)


class EntryItem(object):
    def __init__(self, entry, display_func):
        self.entry = entry
        self.display_func = display_func

    def display(self, driver):
        self.display_func(driver, self.entry)
        time.sleep(5)


if __name__ == '__main__':
    driver = None
    try:
        codepen_picks_feed_url = 'http://codepen.io/picks/feed'
        codepen_popular_feed_url = 'http://codepen.io/popular/feed'
        codepen_recent_feed_url = 'http://codepen.io/recent/feed'
        nasa_image_of_the_day = 'https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss'
        flikr_public_feed = 'https://api.flickr.com/services/feeds/photos_public.gne'
        feeds = [
            # FeedItem(codepen_picks_feed_url, display_codepen),
            # FeedItem(codepen_popular_feed_url, display_codepen),
            # FeedItem(codepen_recent_feed_url, display_codepen),
            # FeedItem(nasa_image_of_the_day, display_nasa_image)
            FeedItem(flikr_public_feed, display_flikr_image)

        ]

        while True:
            entries = []
            for feed in feeds:
                entries.extend(feed.get_entries())

            if any(entries):
                shuffle(entries)

                driver = get_driver()

                while any(entries):
                    entry = entries.pop()
                    entry.display(driver)

    except KeyboardInterrupt:
        pass
    finally:
        if driver:
            driver.quit()
