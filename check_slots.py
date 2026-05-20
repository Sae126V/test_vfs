import requests
from bs4 import BeautifulSoup
import os

URLS = {
    "London Tourism": "https://schengenappointments.com/in/london/tourism",
    "London Business": "https://schengenappointments.com/in/london/switzerland/business",
    "Manchester Business": "https://schengenappointments.com/in/manchester/switzerland/business"
}

def check(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text().lower()

    # NEGATIVE STATE → no slot
    if "no appointments available" in text:
        return False

    # NEGATIVE STATE → no slot
    if "notify me" in text:
        return False

    # ANYTHING ELSE → slot exists
    return True


found = False
centre = ""
url = ""

for c, u in URLS.items():
    if check(u):
        found = True
        centre = c
        url = u
        break

# Write outputs for GitHub Actions
with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
    if found:
        f.write(f"slot=yes\n")
        f.write(f"centre={centre}\n")
        f.write(f"url={url}\n")
    else:
        f.write("slot=no\n")
