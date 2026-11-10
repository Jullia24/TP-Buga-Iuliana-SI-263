# -*- coding: utf-8 -*-
"""Decoder universal (Lucrarea A): recunoaste stratul, il desface, sparge XOR si hash-uri."""
import re
import json
import base64
import hashlib
import argparse
from urllib.parse import unquote

FISA = "arsenal/forensics/fisa.json"


# ---------- A2: recunoastere dupa forma ----------
def ghici_strat(s):
    s = s.strip()
    if re.search(r"%[0-9a-fA-F]{2}", s):                      # 1) URL (are %xx)
        return "url"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:  # 2) hex (mai strict)
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/]+=*", s) and len(s) % 4 == 0:  # 3) base64 (cel mai larg)
        return "base64"
    return "necunoscut"


# ---------- A3: desfacerea unui strat ----------
def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64":
        return strat, base64.b64decode(s)
    if strat == "hex":
        return strat, bytes.fromhex(s)
    if strat == "url":
        return strat, unquote(s).encode()
    return strat, s.encode()


# ---------- A4: straturi multiple ----------
def citibil(b):
    return all(32 <= c < 127 for c in b)


def desfa_straturi(val, maxim=8):
    """Desface in bucla. Intoarce (lista_straturi, rezultat_bytes).
    Un strat nou se accepta doar daca rezultatul e text citibil (primul strat
    poate fi si binar); altfel ne oprim si pastram ultimul rezultat bun."""
    straturi = []
    b = val.encode()
    for _ in range(maxim):
        strat, nou = desfa(val)
        if strat == "necunoscut":
            break
        if straturi and not citibil(nou):
            break
        straturi.append(strat)
        b = nou
        if not citibil(b):
            break
        val = b.decode()
    return straturi, b


# ---------- A5: XOR cu cheie de un octet ----------
def scor_text(t):
    """Cat de mult seamana cu text (litere, cifre, spatii, punctuatie uzuala)."""
    bune = sum(c.isalnum() or c in " .,!-_{}" for c in t)
    return bune / len(t)


def sparge_xor(date):
    """Incearca toate cele 256 de chei. Pastreaza cheile cu rezultat imprimabil,
    ordonate dupa cat seamana cu text (cel mai bun primul)."""
    gasite = []
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            gasite.append((k, clar.decode()))
    gasite.sort(key=lambda kt: scor_text(kt[1]), reverse=True)
    return gasite


# ---------- A6: hash prin dictionar ----------
ALGO = {32: "md5", 40: "sha1", 64: "sha256"}


def sparge_hash(tinta, cale_wordlist):
    algo = ALGO.get(len(tinta))
    if algo is None:
        return None, None
    for cuv in open(cale_wordlist, encoding="latin1"):
        cuv = cuv.strip()
        if hashlib.new(algo, cuv.encode()).hexdigest() == tinta:
            return algo, cuv
    return algo, None


# ---------- A7: linia de comanda + fisa JSON ----------
def salveaza_fisa(date):
    with open(FISA, "w", encoding="utf-8") as f:
        json.dump(date, f, indent=2, ensure_ascii=False)
    print("fisa salvata in", FISA)


def main():
    p = argparse.ArgumentParser(description="Decoder universal: straturi, XOR, hash")
    p.add_argument("intrare", nargs="?", help="sir sau (cu --fisier) cale de fisier")
    p.add_argument("--fisier", action="store_true", help="intrarea este o cale de fisier")
    p.add_argument("--xor", metavar="CALE", help="sparge un fisier XOR cu cheie de un octet")
    p.add_argument("--hash", metavar="CALE", help="fisier cu hash-uri de spart")
    p.add_argument("--wordlist", default="probe/wordlist.txt")
    a = p.parse_args()

    if a.xor:
        gasite = sparge_xor(open(a.xor, "rb").read())
        print(f"{len(gasite)} chei dau rezultat imprimabil; cea mai buna (dupa scor):")
        for k, t in gasite[:3]:
            print(f"cheie: {k} (0x{k:02x})  text: {t}")
        salveaza_fisa({"tip": "xor", "rezultate": [{"cheie": k, "text": t} for k, t in gasite]})
    elif a.hash:
        rez = []
        for linie in open(a.hash):
            h = linie.strip()
            if not h:
                continue
            algo, parola = sparge_hash(h, a.wordlist)
            print(f"{h}  [{algo}]  ->  {parola}")
            rez.append({"hash": h, "algoritm": algo, "parola": parola})
        salveaza_fisa({"tip": "hash", "rezultate": rez})
    elif a.intrare:
        sir = open(a.intrare).read().strip() if a.fisier else a.intrare
        straturi, b = desfa_straturi(sir)
        print("straturi:", " -> ".join(straturi) or "(niciunul)")
        print("rezultat:", b.decode(errors="replace"))
        salveaza_fisa({"strat": straturi, "rezultat": b.decode(errors="replace")})
    else:
        p.print_help()


if __name__ == "__main__":
    main()
