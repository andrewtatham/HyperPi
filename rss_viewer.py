import pprint
import feedparser
import time
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random import shuffle


def display_codepen(driver, entry):
    pprint.pprint(entry)
    entry_fullscreen_url = entry['link'].replace('/pen/', '/full/')
    print(entry_fullscreen_url)
    driver.get(entry_fullscreen_url)
    time.sleep(120)


if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument('--kiosk')  # fullscreen
    # failed attempt to remove the warning message
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--test-type')

    os_name = platform.system()
    print(os_name)
    is_linux = os_name == "Linux"
    if is_linux:
        executable_path = '/usr/lib/chromium-browser/chromedriver'
        driver = webdriver.Chrome(
            executable_path=executable_path,
            chrome_options=chrome_options
        )
    else:
        driver = webdriver.Chrome(
            chrome_options=chrome_options
        )

    try:
        codepen_picks_feed_url = 'https://codepen.io/picks/feed'
        codepen_popular_feed_url = 'https://codepen.io/popular/feed'
        codepen_recent_feed_url = 'https://codepen.io/recent/feed'

        urls = [
            codepen_picks_feed_url,
            codepen_popular_feed_url,
            codepen_recent_feed_url
        ]
        while True:
            entries = []
            for url in urls:
                feed = feedparser.parse(url)
                entries.extend(feed.entries)

            if any(entries):
                shuffle(entries)
                for entry in entries:
                    display_codepen(driver, entry)

    finally:
        driver.quit()
