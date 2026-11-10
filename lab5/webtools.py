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

TIMEOUT = 10
DEFAULT_HEADERS = {"User-Agent": "WebLab-Buga Iuliana"}

def fetch(url: str, timeout: int = TIMEOUT):
    """Descărcare și returnare obiect răspuns folosind antetele implicite."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)

def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
    return response.status_code

def get_title(html: str) -> str:
    """Extrage și returnează titlul unei pagini HTML."""
    start_idx = html.find("<title>") + len("<title>")
    end_idx = html.find("</title>")
    if start_idx != -1 and end_idx != -1:
        return html[start_idx:end_idx].strip()
    return "Fără titlu"

def security_headers(url: str) -> dict:
    """Verifică prezența celor 5 antete de securitate."""
    headers_to_check = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]
    try:
        res = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
        return {h: h in res.headers for h in headers_to_check}
    except requests.RequestException:
        return {h: False for h in headers_to_check}

def score_headers(results: dict) -> str:
    """Calculează scorul de securitate sub formă de șir (ex: '3/5')."""
    total = len(results)
    passed = sum(1 for val in results.values() if val)
    return f"{passed}/{total}"

def fetch_robots(base: str):
    """Returnează textul fișierului /robots.txt sau None."""
    try:
        res = requests.get(base + "/robots.txt", headers=DEFAULT_HEADERS, timeout=TIMEOUT)
        if res.status_code == 200:
            return res.text
    except requests.RequestException:
        pass
    return None

def disallowed_paths(robots_text: str) -> list:
    """Extrage căile interzise din textul robots.txt."""
    if not robots_text:
        return []
    paths = []
    for line in robots_text.splitlines():
        if line.strip().lower().startswith("disallow:"):
            path_val = line.split(":", 1)[1].strip()
            if path_val:
                paths.append(path_val)
    return paths

def check_paths(base: str, paths: list) -> dict:
    """Verifică o listă de căi și returnează un dicționar cu perechile {path: status_code}."""
    results = {}
    for path in paths:
        url = base + path
        try:
            res = requests.get(url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
            results[path] = res.status_code
        except requests.RequestException:
            results[path] = None
        time.sleep(1)
    return results

def resolve(hostname: str) -> str:
    """Returnează adresa IP a unui domeniu."""
    return socket.gethostbyname(hostname)

def cert_days_left(hostname: str) -> int:
    """Returnează zilele rămase până la expirarea certificatului SSL."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expiry_date = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
            return (expiry_date - datetime.utcnow()).days

class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)

def site_report(url: str):
    """Colectează toate informațiile despre site și generează raportul final (afișare + salvare în JSON)."""
    parsed_base = urllib.parse.urlparse(url)
    domain = parsed_base.netloc
    
    # 1. Status și URL final (cu urmărire redirecționări de pe http://)
    http_url = f"http://{domain}"
    try:
        history_res = requests.get(http_url, headers=DEFAULT_HEADERS, timeout=TIMEOUT)
        final_url = history_res.url
        status_code = history_res.status_code
        
        # Construim lanțul de redirecționări corect
        chain_parts = []
        for resp in history_res.history:
            chain_parts.append(str(resp.status_code))
            chain_parts.append(resp.url)
        chain_parts.append(str(history_res.status_code))
        chain_parts.append(history_res.url)
        
        redirect_chain = " -> ".join(chain_parts)
    except requests.RequestException:
        res_direct = fetch(url)
        final_url = res_direct.url
        status_code = res_direct.status_code
        redirect_chain = "Nespecificat"
    
    time.sleep(1)
    page_res = fetch(url)
    
    # 2. Titlu
    title = get_title(page_res.text)
    
    # 3. Adresă IP
    try:
        ip_addr = resolve(domain)
    except socket.gaierror:
        ip_addr = "Indisponibil"
        
    # 4. Scor securitate
    sec_dict = security_headers(url)
    sec_score = score_headers(sec_dict)
    time.sleep(1)
    
    # 5. Certificat
    try:
        days_left = cert_days_left(domain)
    except Exception:
        days_left = "Indisponibil"
        
    # 6. Legături interne și externe
    links = re.findall(r'href="([^"]+)"', page_res.text)
    internal_count = 0
    external_count = 0
    for l in links:
        full = urllib.parse.urljoin(url, l)
        p = urllib.parse.urlparse(full)
        if p.netloc == domain or p.netloc == "":
            internal_count += 1
        else:
            external_count += 1
            
    # 7. Căi interzise robots.txt
    robots_content = fetch_robots(f"{parsed_base.scheme}://{domain}")
    disallowed = disallowed_paths(robots_content)
    
    # Afișare rezultat
    print(f"=== Raport site: {url} ===")
    print(f"Cod de stare:      {status_code}")
    print(f"Titlu:             {title}")
    print(f"Adresă IP:         {ip_addr}")
    print(f"Redirecționări:    {redirect_chain}")
    print(f"Scor securitate:   {sec_score}")
    print(f"Certificat:        {days_left} zile rămase" if isinstance(days_left, int) else f"Certificat:        {days_left}")
    print(f"Legături:          {internal_count} interne, {external_count} externe")
    print(f"Căi interzise:     {', '.join(disallowed) if disallowed else 'Niciuna'}")
    print("Salvat în report.json")
    
    # Salvare în report.json
    report_data = {
        "url": url,
        "status_code": status_code,
        "title": title,
        "ip_address": ip_addr,
        "security_score": sec_score,
        "cert_days_left": days_left,
        "internal_links": internal_count,
        "external_links": external_count,
        "disallowed_paths": disallowed
    }
    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)

if __name__ == "__main__":
    print("Autotest:", get_status("https://cybercor.org"))