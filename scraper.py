import time
import os
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Setup headless Chrome
chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

try:
    # Go to Reddit search page
    url = 'https://www.reddit.com/r/anime/search/?q=top+10+anime+"Anime+Corner"&type=posts&sort=new'
    driver.get(url)
    time.sleep(3)  # Let the page load a bit

    # Scroll to load posts
    for _ in range(5):
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(1.5)

    # Find first post title link
    posts = driver.find_elements(By.CSS_SELECTOR, '[data-testid="search-sdui-post"] [data-testid="post-title"]')
    if not posts:
        raise Exception("No posts found.")

    posts[0].click()
    time.sleep(5)  # Wait for post to load

    # Try to find image
    image = driver.find_element(By.CSS_SELECTOR, 'img[alt*="Image"]')  # fallback selector
    image_url = image.get_attribute('src')
    print("Found image:", image_url)

    # Optionally post to Discord
    discord_webhook = os.getenv("DISCORD_WEBHOOK")
    if discord_webhook and image_url:
        requests.post(discord_webhook, json={
            "username": "Anime",
            "avatar_url": "https://styles.redditmedia.com/t5_2qh22/styles/communityIcon_18jg89hnk9ae1.png",
            "content": image_url
        })

except (TimeoutException, NoSuchElementException) as e:
    print("Error:", e)

finally:
    driver.quit()
