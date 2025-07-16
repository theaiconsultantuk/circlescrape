import time
import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# --- Configuration ---
COOKIE_FILE = '/Users/paulcowen/Library/CloudStorage/GoogleDrive-info@cluehqbrentwood.co.uk/My Drive/1-Work/11-AI-Artificial-Intelligence/Skool Scripts/Andy/Andy_Circle_Cookies.txt'
TARGET_URL = 'https://community.theaiautomators.com/c/automation-templates/'
OUTPUT_JSON = 'automation_templates_links.json'

def read_netscape_cookies(filepath):
    """Reads a Netscape-format cookie file and returns a list of cookie dicts."""
    cookies = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 7:
                domain, flag, path, secure, expiry, name, value = parts[:7]
                cookies.append({
                    'domain': domain,
                    'name': name,
                    'value': value,
                    'path': path,
                    'secure': secure == 'TRUE',
                    'expiry': int(expiry) if expiry.isdigit() else 0
                })
    return cookies

def main():
    print('--- Starting Circle Automation Templates Scraper ---')
    if not os.path.exists(COOKIE_FILE):
        print(f'[ERROR] Cookie file not found at: {COOKIE_FILE}')
        return

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")  # Remove this line if you want to see the browser
    driver = webdriver.Chrome(service=service, options=options)

    print('[INFO] Navigating to theaiautomators.com to set cookies...')
    driver.get('https://community.theaiautomators.com')

    print(f'[INFO] Reading cookies from {COOKIE_FILE}...')
    cookies = read_netscape_cookies(COOKIE_FILE)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"[WARNING] Could not set cookie {cookie.get('name')}: {str(e)}")

    print(f'[INFO] Navigating to target URL: {TARGET_URL}')
    driver.get(TARGET_URL)
    time.sleep(3)  # Allow page to load

    # Scrape post cards
    print('[INFO] Scraping post cards...')
    post_cards = driver.find_elements(By.CSS_SELECTOR, 'div.post--card.post--parent')
    results = []
    for card in post_cards:
        try:
            title_link = card.find_element(By.CSS_SELECTOR, 'h2 a')
            title = title_link.text.strip()
            href = title_link.get_attribute('href')
            if href and href.startswith('/'):
                href = 'https://community.theaiautomators.com' + href
            results.append({'title': title, 'url': href})
        except Exception as e:
            print(f"[WARNING] Could not extract title/url from a card: {str(e)}")
            continue

    # Save to JSON
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f'[INFO] Saved {len(results)} links to {OUTPUT_JSON}')

    driver.quit()

if __name__ == '__main__':
    main()
