import pprint
import feedparser
import time
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def display_codepen(driver, entry):
    url = entry['link'].replace('/pen/', '/full/')
    print(url)
    driver.get(url)
    time.sleep(30)


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
        feed = feedparser.parse(codepen_picks_feed_url)
        pprint.pprint(feed)
        for entry in feed.entries:
            display_codepen(driver, entry)

    finally:
        driver.quit()
