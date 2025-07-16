import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
COOKIE_FILE = '/Users/paulcowen/Library/CloudStorage/GoogleDrive-info@cluehqbrentwood.co.uk/My Drive/1-Work/11-AI-Artificial-Intelligence/Skool Scripts/Andy/Andy_Circle_Cookies.txt'
TARGET_URL = 'https://community.theaiautomators.com/c/automation-templates/'

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
    """Launches Chrome, injects cookies, and navigates to the target URL."""
    print('--- Starting Circle Debug Browser ---')
    if not os.path.exists(COOKIE_FILE):
        print(f'[ERROR] Cookie file not found at: {COOKIE_FILE}')
        return

    print('[INFO] Setting up Chrome driver...')
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the domain to set cookies
    print('[INFO] Navigating to theaiautomators.com to set cookies...')
    driver.get('https://community.theaiautomators.com')

    # Inject cookies
    print(f'[INFO] Reading cookies from {COOKIE_FILE}...')
    cookies = read_netscape_cookies(COOKIE_FILE)
    for cookie in cookies:
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"[WARNING] Could not set cookie {cookie.get('name')}: {str(e)}")
    print(f'[INFO] Injected {len(cookies)} cookies.')

    # Navigate to the target URL
    print(f'[INFO] Navigating to target URL: {TARGET_URL}')
    driver.get(TARGET_URL)

    print('\n--- Browser is ready for inspection ---')
    print('The browser will remain open. Please inspect the page to find the correct CSS selector.')
    print('Close the browser window manually when you are finished.')

    # Keep the browser open until manually closed
    while True:
        try:
            # Check if the browser is still open
            driver.title
            time.sleep(1)
        except Exception:
            # Browser has been closed
            print('\n--- Debug browser closed. ---')
            break

if __name__ == '__main__':
    main()