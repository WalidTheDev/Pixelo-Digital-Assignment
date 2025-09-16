import requests
from bs4 import BeautifulSoup
import re

def scrape_emails(url):
    emails = set()
    
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if response.status_code != 200:
            print("Failed to fetch page")
            return emails

        # regex
        emails.update(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", response.text))

        # check links
        soup = BeautifulSoup(response.text, "html.parser")
        for a in soup.find_all("a", href=True):
            if "mailto:" in a["href"]:
                emails.add(a["href"].replace("mailto:", "").strip())

    except Exception as e:
        print("Error:", e)

    return emails


if __name__ == "__main__":
    url = r"https://krishnakushwaha.netlify.app/" # Sample url
    found_emails = scrape_emails(url)
    
    if found_emails:
        print(" Emails found:")
        for email in found_emails:
            print(email)
    else:
        print("No emails found.")
