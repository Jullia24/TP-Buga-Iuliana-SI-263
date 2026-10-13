import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]

def build_url(host, path):
    return f"https://{host.strip('/')}/{path.lstrip('/')}"

def is_https(url):
    return url.startswith("https://")

def show_response(url):
    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
    except requests.RequestException as e:
        print(f"Eroare: {e}")

def check_site(url):
    try:
        response = requests.get(url, timeout=5)
        ct = response.headers.get('Content-Type', '')
        if ';' in ct:
            ct = ct.split(';')[0].strip()
        return {
            "status": response.status_code,
            "content_type": ct if ct else None,
            "length": len(response.content),
            "server": response.headers.get('Server', 'unknown')
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(e)}

def scan_sites():
    success_count = 0
    fail_count = 0
    valid_results = []

    for url in SITES:
        res = check_site(url)
        if res.get("status") == 200:
            success_count += 1
            valid_results.append((url, res.get("length", 0)))
        else:
            fail_count += 1

    valid_results.sort(key=lambda x: x[1], reverse=True)

    for url, length in valid_results:
        print(f"{url} -> 200, {length} octeți")

    print(f"Reușite: {success_count} Eșuate: {fail_count}")

def check_headers(url):
    pass

def retry_check(url, attempts=3):
    pass
