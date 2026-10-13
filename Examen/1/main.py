from checker import (
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check
)

# Partea 1: apeluri pentru build_url și is_https
print("--- Partea 1: Funcții ajutătoare ---")
print("build_url (fără /):", build_url("example.com", "login"))
print("build_url (cu /):", build_url("example.com", "/login"))
print("is_https (https):", is_https("https://example.com"))
print("is_https (http):", is_https("http://example.com"))

# Partea 2: apeluri pentru show_response
print("\n--- Partea 2: Trimiterea unei cereri ---")
show_response("https://example.com")

# Partea 3: apeluri pentru check_site
print("\n--- Partea 3: Verificator reutilizabil ---")
print("check_site (valid):", check_site("https://example.com"))
print("check_site (invalid):", check_site("http://this-site-does-not-exist.invalid"))

# Partea 4: apelul scan_sites()
print("\n--- Partea 4: Verificarea mai multor site-uri ---")
scan_sites()

