import requests
from bs4 import BeautifulSoup

URLS = {
    "London Tourism": "https://schengenappointments.com/in/london/tourism",
    "London Business": "https://schengenappointments.com/in/london/switzerland/business",
    "Manchester Business": "https://schengenappointments.com/in/manchester/switzerland/business",
    "Edinburgh Business": "https://schengenappointments.com/in/edinburgh/switzerland/business"
}

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

    if "notify me" in text:
        return False

    return any(state in text for state in POSITIVE_STATES)

found = False
centre = ""
url = ""

for c, u in URLS.items():
    if check(u):
        found = True
        centre = c
        url = u
        break

# NEW GitHub Actions output format
with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
    if found:
        f.write(f"slot=yes\n")
        f.write(f"centre={centre}\n")
        f.write(f"url={url}\n")
    else:
        f.write("slot=no\n")
