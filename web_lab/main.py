# Laborator: funcții, metode și importuri pe web
# Student: Buga Iuliana

import sys
import argparse
import csv
from datetime import datetime
import time
import webtools

def main():
    # Exercițiul 45 explicat în comentariu:
    # Dacă în main.py am defini propria funcție cu același nume (de ex. get_title), 
    # Python ar folosi funcția definită local în main.py în loc de cea importată din webtools.py (suprascriere locală).
    
    # Exercițiul 47: Afișare constantă de modul importată
    print("Constanta DEFAULT_HEADERS:", webtools.DEFAULT_HEADERS)
    
    # Exercițiul 48: Argumente din linia de comandă cu argparse
    parser = argparse.ArgumentParser(description="Generează raport web pentru un URL.")
    parser.add_argument("url", nargs="?", default="https://cybercor.org", help="URL-ul țintă")
    args = parser.parse_args()
    
    target_url = args.url
    print(f"Se rulează analizele pentru: {target_url}\n")
    
    # Exercițiul 44 & 50: Apelarea funcțiilor din modulul propriu
    # 1. Rulare proiect final (generează report.json)
    webtools.site_report(target_url)
    
    # 2. Exercițiul 49: Salvarea rezultatului funcției check_paths() în report.csv
    print("\nSe generează report.csv...")
    paths_to_check = ["/", "/robots.txt", "/sitemap.xml"]
    parsed_u = webtools.urllib.parse.urlparse(target_url)
    base_domain = f"{parsed_u.scheme}://{parsed_u.netloc}"
    
    path_results = webtools.check_paths(base_domain, paths_to_check)
    
    with open("report.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["path", "status", "checked_at"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        checked_timestamp = datetime.now().isoformat()
        for p, status in path_results.items():
            writer.writerow({
                "path": p,
                "status": status,
                "checked_at": checked_timestamp
            })
    print("Salvat în report.csv")

if __name__ == "__main__":
    main()

# Răspuns la întrebarea legată de blocul if __name__ == "__main__": (Exercițiul 46):
# Autotestul rulează doar atunci când rulezi scriptul direct din terminal cu 'python3 webtools.py', 
# deoarece variabila specială __name__ devine "__main__". 
# Când importi fișierul în main.py ('import webtools'), __name__ ia valoarea "webtools", 
# iar blocul respectiv este ignorat, prevenind rularea nedorită a autotestului la fiecare import.