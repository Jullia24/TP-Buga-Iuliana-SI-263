# Laborator: funcții, metode și importuri pe web
# Student: Buga Iuliana

import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Exercițiul 9. Elementele de bază ale răspunsului
print("--- Exercițiul 9 ---")
response = requests.get(BASE_URL, timeout=TIMEOUT)
print("status_code:", response.status_code, "(Atribut)")
print("ok:", response.ok, "(Atribut)")
print("url:", response.url, "(Atribut)")
print("encoding:", response.encoding, "(Atribut)")
time.sleep(1)

# Exercițiul 10. Tratarea erorilor cu o metodă
print("\n--- Exercițiul 10 ---")
try:
    response.raise_for_status()
    print("Pagina principală s-a încărcat cu succes.")
    
    bad_response = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    bad_response.raise_for_status()
except requests.HTTPError as e:
    print("Eroare HTTP capturată cu succes (mesaj prietenos): Pagina căutată nu există sau a apărut o problemă temporară.")
time.sleep(1)

# Exercițiul 11. Toate antetele
print("\n--- Exercițiul 11 ---")
for name, value in response.headers.items():
    print(f"{name}: {value}")

# Exercițiul 12. Metode de dicționar
print("\n--- Exercițiul 12 ---")
print("Server:", response.headers.get("Server", "lipsește"))
print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
print("content-type (cu litere mici):", response.headers.get("content-type", "lipsește"))

# Exercițiul 13. Înlănțuirea metodelor de șir
print("\n--- Exercițiul 13 ---")
cyber_count = response.text.lower().count("cyber")
print("De câte ori apare 'cyber':", cyber_count)

# Exercițiul 14. Găsirea titlului
print("\n--- Exercițiul 14 ---")
html = response.text
start_idx = html.find("<title>") + len("<title>")
end_idx = html.find("</title>")
if start_idx != -1 and end_idx != -1:
    title = html[start_idx:end_idx].strip()
    print("Titlu extras:", title)

# Exercițiul 15. Numărarea liniilor
print("\n--- Exercițiul 15 ---")
lines = html.splitlines()
print("Număr total de linii:", len(lines))
longest_line = max(lines, key=len)
print("Lungimea celei mai lungi linii:", len(longest_line))

# Exercițiul 16. Verificarea HTTPS
print("\n--- Exercițiul 16 ---")
if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")

# Exercițiul 17. Urmărirea redirecționărilor
print("\n--- Exercițiul 17 ---")
redirect_response = requests.get("http://cybercor.org", timeout=TIMEOUT)
for hist in redirect_response.history:
    print(f"Status: {hist.status_code} -> URL: {hist.url}")
print("URL final:", redirect_response.url)
time.sleep(1)

# Exercițiul 18. HEAD versus GET
print("\n--- Exercițiul 18 ---")
head_res = requests.head(BASE_URL, timeout=TIMEOUT)
get_res = requests.get(BASE_URL, timeout=TIMEOUT)
print("Lungime conținut HEAD:", len(head_res.content))
print("Lungime conținut GET:", len(get_res.content))
time.sleep(1)

# Exercițiul 19. Cookie-uri
print("\n--- Exercițiul 19 ---")
if len(response.cookies) == 0:
    print("Niciun cookie setat")
else:
    for cookie in response.cookies:
        print(f"Cookie: {cookie.name}, Secure: {cookie.secure}")

# Exercițiul 20. Sesiuni
print("\n--- Exercițiul 20 ---")
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-Buga Iuliana"})
session_res = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print("Răspuns de la echo headers:\n", session_res.text)
