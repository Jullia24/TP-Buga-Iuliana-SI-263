import argparse
import json
import os

GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}

def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        return [linie.strip() for linie in f if linie.strip() and not linie.strip().startswith("#")]

def nume(cale):
    return cale.rsplit("/", 1)[-1]

def suid_constatari(cale):
    cai = citeste_linii(cale)
    cai_unice = sorted(list(set(cai)))
    out = []
    for c in cai_unice:
        n = nume(c)
        risc = "mare" if n in GTFO else "normal"
        out.append({"cale": c, "nume": n, "risc": risc})
    return out

def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        if " : " in ln:
            user, drept = ln.split(" : ", 1)
            risc = "mare" if "NOPASSWD" in drept else "normal"
            out.append({"user": user.strip(), "drept": drept.strip(), "risc": risc})
    return out

def cron_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        if len(campuri) >= 7:
            user = campuri[5]
            comanda = " ".join(campuri[6:])
            out.append({"user": user, "comanda": comanda})
    return out

def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt")),
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    
    raport = enumereaza(a.capturi)
    
    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return
        
    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") == "mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")
        
    useri_sudo = {c["user"] for c in raport["sudo"]}
    useri_cron = {c["user"] for c in raport["cron"]}
    utilizatori_implicati = sorted(list(useri_sudo | useri_cron))
    print(f"utilizatori implicati: {', '.join(utilizatori_implicati)}")
    
    with open("arsenal/lab8/enum.json", "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")