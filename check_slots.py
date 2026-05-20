import requests
from bs4 import BeautifulSoup

URLS = {
    "London Tourism": "https://schengenappointments.com/in/london/tourism",
    "London Business": "https://schengenappointments.com/in/london/switzerland/business",
    "Manchester Business": "https://schengenappointments.com/in/manchester/switzerland/business",
    "Edinburgh Business": "https://schengenappointments.com/in/edinburgh/switzerland/business"
}

# Any of these means "slot available"
POSITIVE_STATES = [
    "available",
    "slots",
    "waiting list",
    "open",
    "few",
    "limited"
]

def check(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text().lower()

    # Ignore "notify me"
    if "notify me" in text:
        return False

    # Match any positive state
    return any(state in text for state in POSITIVE_STATES)

found = False
found_centre = ""
found_url = ""

for centre, url in URLS.items():
    if check(url):
        found = True
        found_centre = centre
        found_url = url
        break

if found:
    print("::set-output name=slot::yes")
    print(f"::set-output name=centre::{found_centre}")
    print(f"::set-output name=url::{found_url}")
else:
    print("::set-output name=slot::no")
