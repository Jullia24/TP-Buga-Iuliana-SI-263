# Laborator: funcții, metode și importuri pe web
# Student: Buga Iuliana

import requests
import time
import urllib.parse
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
from datetime import datetime

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# Exercițiul 35. Descompunerea unui URL
print("--- Exercițiul 35 ---")
parsed_url = urllib.parse.urlparse("https://cybercor.org/path?x=1#top")
print("scheme:", parsed_url.scheme)
print("netloc:", parsed_url.netloc)
print("path:", parsed_url.path)
print("query:", parsed_url.query)
print("fragment:", parsed_url.fragment)

# Exercițiul 36. Compunerea URL-urilor
print("\n--- Exercițiul 36 ---")
for rel in ["/about", "contact.html", "../index.html"]:
    print(urllib.parse.urljoin(BASE_URL, rel))

# Exercițiul 37. Extragerea legăturilor
def extract_links(html: str) -> list:
    """Extrage toate legăturile unice dintr-un șir HTML."""
    links = re.findall(r'href="([^"]+)"', html)
    return list(set(links))

print("\n--- Exercițiul 37 ---")
res_ex37 = requests.get(BASE_URL, timeout=TIMEOUT)
print("Legături unice:", extract_links(res_ex37.text)[:5]) # Primele 5
time.sleep(1)

# Exercițiul 38. Interne sau externe?
def split_links(links: list, domain: str) -> tuple:
    """Împarte legăturile în interne (același domeniu) și externe."""
    internal = []
    external = []
    for link in links:
        full_url = urllib.parse.urljoin(BASE_URL, link)
        parsed = urllib.parse.urlparse(full_url)
        if parsed.netloc == domain or parsed.netloc == "":
            internal.append(link)
        else:
            external.append(link)
    return internal, external

print("\n--- Exercițiul 38 ---")
sample_links = ["/about", "https://google.com", "contact.html"]
print(split_links(sample_links, "cybercor.org"))

# Exercițiul 39. Propriile metode (Clasa ImageFinder)
class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)

print("\n--- Exercițiul 39 (Test) ---")
test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""
finder = ImageFinder()
finder.feed(test_html)
assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp",
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul a trecut cu succes!")

# Rulare pe site-ul real
response_img = requests.get(BASE_URL, timeout=TIMEOUT)
finder_real = ImageFinder()
finder_real.feed(response_img.text)
print(len(finder_real.images), "imagini găsite pe site-ul real.")
time.sleep(1)

# Exercițiul 40. Amprenta paginii
def page_fingerprint(url: str) -> str:
    """Calculează amprenta SHA-256 a conținutului unei pagini."""
    res = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(res.content).hexdigest()

print("\n--- Exercițiul 40 ---")
print("Amprentă 1:", page_fingerprint(BASE_URL))
time.sleep(1)
print("Amprentă 2:", page_fingerprint(BASE_URL))
# Amprentele ar fi diferite dacă conținutul paginii s-a modificat între cele două cereri (ex: articole noi, știri, ceas dinamic).
time.sleep(1)

# Exercițiul 41. Salvarea în JSON
print("\n--- Exercițiul 41 ---")
res_headers = requests.get(BASE_URL, timeout=TIMEOUT)
with open("headers.json", "w", encoding="utf-8") as f:
    json.dump(dict(res_headers.headers), f, indent=2)

with open("headers.json", "r", encoding="utf-8") as f:
    loaded_headers = json.load(f)
print("Antet Server din JSON:", loaded_headers.get("Server"))
time.sleep(1)

# Exercițiul 42. Interogare DNS
def resolve(hostname: str) -> str:
    """Returnează adresa IP pentru un hostname dat."""
    return socket.gethostbyname(hostname)

print("\n--- Exercițiul 42 ---")
print("IP pentru cybercor.org:", resolve("cybercor.org"))

# Exercițiul 43. Expirarea certificatului
def cert_days_left(hostname: str) -> int:
    """Returnează numărul de zile rămase până la expirarea certificatului SSL."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            not_after = cert["notAfter"]
            # Parsarea datei de expirare (formatul furnizat de getpeercert este de tipul: 'May 17 12:00:00 2024 GMT')
            expiry_date = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
            delta = expiry_date - datetime.utcnow()
            return delta.days
print("\n--- Exercițiul 43 ---")
try:
    print("Zile rămase certificat:", cert_days_left("cybercor.org"))
except Exception as e:
    print("Eroare la citirea certificatului:", e)

# Răspuns la întrebarea de verificare: În exercițiul 39, metoda handle_starttag() este apelată automat 
# de către motorul intern al clasei părinte HTMLParser atunci când apelezi metoda .feed() pe un text HTML.