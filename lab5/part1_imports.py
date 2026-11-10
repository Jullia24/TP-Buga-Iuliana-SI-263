# Laborator: funcții, metode și importuri pe web
# Student: Buga Iuliana

import requests
import urllib.request
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Exercițiul 1. Primul import
print("--- Exercițiul 1 ---")
print("Versiune requests:", requests.__version__)
import urllib.request

# Exercițiul 2. Două stiluri de import
print("\n--- Exercițiul 2 ---")
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("Cod stare (stil 1):", response.status_code)

from requests import get
response_from = get(BASE_URL, timeout=TIMEOUT)
print("Cod stare (stil 2):", response_from.status_code)

# Exercițiul 3. Alias-uri
print("\n--- Exercițiul 3 ---")
import requests as rq
response_alias = rq.get(BASE_URL, timeout=TIMEOUT)
print("Cod stare cu alias:", response_alias.status_code)

# Exercițiul 4. Doar biblioteca standard
print("\n--- Exercițiul 4 ---")
import ssl

ssl_context = ssl._create_unverified_context()

req = urllib.request.Request(
    BASE_URL, 
    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
)

with urllib.request.urlopen(req, timeout=TIMEOUT, context=ssl_context) as std_response:
    print("Status urllib:", std_response.status)
    body_part = std_response.read(200).decode("utf-8")
    print("Primele 200 caractere:", body_part)

# Exercițiul 5. Priviți în interiorul unui modul
print("\n--- Exercițiul 5 ---")


# Exercițiul 6. Citiți documentația
print("\n--- Exercițiul 6 ---")
# help(requests.get)
response_timeout = requests.get(BASE_URL, timeout=5)
print("Cerere cu timeout explicit reușită:", response_timeout.status_code)

# Exercițiul 7. Cronometrarea unei cereri
print("\n--- Exercițiul 7 ---")
start_time = time.perf_counter()
res_timed = requests.get(BASE_URL, timeout=TIMEOUT)
end_time = time.perf_counter()
print("Timp măsurat cu perf_counter:", end_time - start_time, "secunde")
print("Timp din response.elapsed:", res_timed.elapsed.total_seconds(), "secunde")

# Exercițiul 8. Când un import eșuează
print("\n--- Exercițiul 8 ---")
try:
    import bs4
    print("Modulul bs4 este instalat.")
except ImportError:
    print("Instalați modulul cu: pip install beautifulsoup4")