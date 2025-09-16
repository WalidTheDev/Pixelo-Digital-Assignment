from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time


OUTPUT_FILE = "500co_companies_selenium.csv"
# URL = "https://500.co/companies"
page_no = 221
URL = f"https://500.co/portfolio?industry=all&region=all&stage=all&country=all&bModel=all&batch=all&&page={str(page_no)}&sort=alphabetically#companies-table"


def scrape_companies(URL):
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # uncomment to run in background
    driver = webdriver.Chrome(options=options)

    try:
        print(f"[*] Opening {URL}")
        driver.get(URL)

        # Wait longer for first page to load
        print("[*] Waiting for page to fully load (10s)...")
        time.sleep(10)


        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.w-full.flex.p-4")))

        cards_seen = 0
        stable_scrolls = 0

        while True:
            # Get current cards
            cards = driver.find_elements(By.CSS_SELECTOR, "div.w-full.flex.p-4")
            count = len(cards)

            if count > cards_seen:
                cards_seen = count
                print(f"[*] Found {cards_seen} cards so far...")
                stable_scrolls = 0
            else:
                stable_scrolls += 1
                if stable_scrolls >= 5:
                    print("[*] No more new cards detected. Stopping scroll.")
                    break

            # Scroll down and wait for more cards to load
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)

        # Now extract details
        rows = []
        for card in cards:
            try:
                try:
                    name = card.find_element(By.TAG_NAME, "h3").text.strip()
                except:
                    name = card.text.split("\n")[0].strip()

                try:
                    link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
                except:
                    link = ""

                rows.append([name, link])
            except:
                continue

        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Company Name", "Description" , "Link"])
            writer.writerows(rows)

        print(f"✅ Done. Scraped {len(rows)} companies. Saved to {OUTPUT_FILE}")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_companies(URL)
