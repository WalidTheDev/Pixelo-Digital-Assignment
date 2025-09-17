from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time


page_no = 221



def scrape_companies(page_no):
    URL = f"https://500.co/portfolio?industry=all&region=all&stage=all&country=all&bModel=all&batch=all&&page={str(page_no)}&sort=alphabetically#companies-table"
    OUTPUT_FILE = "500co_companies_selenium.csv"
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
                    break


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
                
              

                rows.append([name , link])
            except:
                continue

        with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        print(f"✅ Done. Scraped {len(rows)} companies. Saved to {OUTPUT_FILE}")

    finally:
        driver.quit()

def create_file():
    OUTPUT_FILE = "500co_companies_selenium.csv"
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Company Name" , "Link"])
    print("[*] File Created with headings")



if __name__ == "__main__":
    create_file()
    for page_no in range(1,222) :
        print(f"[*] Initialising Scrapping of page Number {str(page_no)}")
        scrape_companies(page_no)