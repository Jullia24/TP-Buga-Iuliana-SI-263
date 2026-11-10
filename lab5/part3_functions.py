# Laborator: funcții, metode și importuri pe web
# Student: Buga Iuliana

import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Exercițiul 21. Prima funcție
def fetch(url: str, timeout: int = TIMEOUT):
    """Descărcare și returnare obiect răspuns pentru un URL dat."""
    return requests.get(url, timeout=timeout)

print("--- Exercițiul 21 ---")
res_ex21 = fetch(BASE_URL)
print("Cod stare fetch:", res_ex21.status_code)
time.sleep(1)

# Exercițiul 22. Returnarea unei singure valori
def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code

print("\n--- Exercițiul 22 ---")
for path in ["/", "/robots.txt", "/sitemap.xml"]:
    url_test = BASE_URL + path
    print(f"URL {path} -> Status:", get_status(url_test))
    time.sleep(1)

# Exercițiul 23. Parametri impliciți
print("\n--- Exercițiul 23 ---")
try:
    res_t3 = fetch(BASE_URL, timeout=3)
    print("Fetch cu timeout=3 reușit:", res_t3.status_code)
except requests.Timeout:
    print("Cererea a expirat.")
time.sleep(1)

# Exercițiul 24. O singură sarcină pe funcție
def get_title(html: str) -> str:
    """Extrage și returnează titlul dintr-un șir HTML."""
    start_idx = html.find("<title>") + len("<title>")
    end_idx = html.find("</title>")
    if start_idx != -1 and end_idx != -1:
        return html[start_idx:end_idx].strip()
    return "Fără titlu"

print("\n--- Exercițiul 24 ---")
print("Titlu extras prin funcție:", get_title(res_ex21.text))

# Exercițiul 25. Docstring-uri
print("\n--- Exercițiul 25 ---")
help(get_title)
print(get_title.__doc__)

# Exercițiul 26. Adnotări de tip
print("\n--- Exercițiul 26 ---")

# Exercițiul 27. Fără opriri neașteptate
def page_exists(url: str) -> bool:
    """Returnează True dacă pagina poate fi accesată fără erori, altfel False."""
    try:
        res = requests.get(url, timeout=TIMEOUT)
        return res.ok
    except requests.RequestException:
        return False

print("\n--- Exercițiul 27 ---")
print("Exista BASE_URL?", page_exists(BASE_URL))
print("Exista domeniul invalid?", page_exists("https://this-domain-does-not-exist.invalid"))
time.sleep(1)

# Exercițiul 28. Returnarea unui dicționar
def check_paths(base: str, paths: list) -> dict:
    """Verifică o listă de căi și returnează un dicționar cu perechile {path: status_code}."""
    results = {}
    for path in paths:
        url = base + path
        try:
            res = requests.get(url, timeout=TIMEOUT)
            results[path] = res.status_code
        except requests.RequestException:
            results[path] = None
        time.sleep(1)
    return results

print("\n--- Exercițiul 28 ---")
print(check_paths(BASE_URL, ["/", "/robots.txt"]))

# Exercițiul 29. Argumente cu nume
def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Returnează valoarea unui singur antet sau valoarea implicită."""
    res = requests.get(url, timeout=TIMEOUT)
    return res.headers.get(name, default)

print("\n--- Exercițiul 29 ---")
print("Antet Server:", get_header(BASE_URL, name="Server"))
time.sleep(1)

# Exercițiul 30. Antete de securitate
def security_headers(url: str) -> dict:
    """Verifică prezența a 5 antete de securitate și returnează un dicționar cu True/False."""
    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    res = requests.get(url, timeout=TIMEOUT)
    result = {}
    for h in headers_to_check:
        result[h] = h in res.headers
    return result

print("\n--- Exercițiul 30 ---")
sec_res = security_headers(BASE_URL)
print(sec_res)
time.sleep(1)

# Exercițiul 31. Funcții care apelează funcții
def score_headers(results: dict) -> str:
    """Calculează scorul de securitate sub formă de șir (ex: '3/5')."""
    total = len(results)
    passed = sum(1 for val in results.values() if val)
    return f"{passed}/{total}"

print("\n--- Exercițiul 31 ---")
print("Scor securitate:", score_headers(security_headers(BASE_URL)))
time.sleep(1)

# Exercițiul 32. Două funcții, o sarcină
def fetch_robots(base: str):
    """Returnează conținutul fișierului robots.txt sau None dacă lipsește."""
    try:
        res = requests.get(base + "/robots.txt", timeout=TIMEOUT)
        if res.status_code == 200:
            return res.text
    except requests.RequestException:
        pass
    return None

def disallowed_paths(robots_text: str) -> list:
    """Extrage liniile Disallow dintr-un text robots.txt."""
    if not robots_text:
        return []
    paths = []
    for line in robots_text.splitlines():
        if line.strip().lower().startswith("disallow:"):
            path_val = line.split(":", 1)[1].strip()
            if path_val:
                paths.append(path_val)
    return paths

print("\n--- Exercițiul 32 ---")
robots_txt = fetch_robots(BASE_URL)
print("Căi interzise:", disallowed_paths(robots_txt))
time.sleep(1)

# Exercițiul 33. Oricâte argumente
def response_times(*urls) -> dict:
    """Măsoară timpul de răspuns pentru oricâte URL-uri primite."""
    times_dict = {}
    for u in urls:
        start = time.perf_counter()
        try:
            requests.get(u, timeout=TIMEOUT)
            elapsed = time.perf_counter() - start
            times_dict[u] = elapsed
        except requests.RequestException:
            times_dict[u] = None
        time.sleep(1)
    return times_dict

print("\n--- Exercițiul 33 ---")
print(response_times(BASE_URL, ECHO_URL))

# Exercițiul 34. Argumente cu nume colectate
def log(message: str, **details):
    """Afișează un mesaj însoțit de detalii suplimentare transmise ca argumente cu nume."""
    details_str = " | ".join(f"{k}={v}" for k, v in details.items())
    if details_str:
        print(f"{message} | {details_str}")
    else:
        print(message)

print("\n--- Exercițiul 34 ---")
log("verificat", url=BASE_URL, status=200)