# -*- coding: utf-8 -*-
"""Lucrarea B (B1-B4): magic bytes, strings, EXIF/GPS, file carving.
Rulare:  python forensics.py B1   (sau B2, B3, B4)"""
import re
import sys
import zipfile
from PIL import Image
from PIL.ExifTags import TAGS


# ---------- B1: tipul real dupa semnatura ----------
def tip_real(cale):
    cap = open(cale, "rb").read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return cap.hex()


def b1():
    for cale in ["probe/foto.jpg", "probe/ascuns.png", "probe/mesaj.txt", "probe/xor.bin"]:
        cap = open(cale, "rb").read(8)
        print(f"{cale:18} primii octeti: {cap.hex(' '):24} -> {tip_real(cale)}")


# ---------- B2: strings ----------
def strings(cale, minim=4):
    date = open(cale, "rb").read()
    return [m.decode() for m in re.findall(rb"[ -~]{%d,}" % minim, date)]


def b2():
    sir = strings("probe/ascuns.png")
    print(f"{len(sir)} secvente imprimabile in probe/ascuns.png; ultimele 4:")
    for s in sir[-4:]:
        print("  ", s)


# ---------- B3: EXIF + GPS ----------
def in_grade_zecimale(dms, ref):
    g, m, s = (float(x) for x in dms)
    val = g + m / 60 + s / 3600
    return -val if ref in ("S", "W") else val


def b3():
    img = Image.open("probe/foto.jpg")
    exif = img.getexif()
    for id, val in exif.items():
        if id == 34853:               # GPSInfo: il tratam separat
            continue
        print(f"{TAGS.get(id, id)} = {val}")
    gps = exif.get_ifd(34853)
    print("GPS brut:", {k: (tuple(float(x) for x in v) if isinstance(v, tuple) else v)
                        for k, v in gps.items()})
    lat = in_grade_zecimale(gps[2], gps[1])
    lon = in_grade_zecimale(gps[4], gps[3])
    print(f"Latitudine : {lat:.4f}")
    print(f"Longitudine: {lon:.4f}")
    print(f"Harta      : https://www.openstreetmap.org/?mlat={lat:.4f}&mlon={lon:.4f}")


# ---------- B4: file carving ----------
def b4():
    date = open("probe/ascuns.png", "rb").read()
    i = date.find(b"PK\x03\x04")
    if i == -1:
        print("nu am gasit nicio arhiva ZIP")
        return
    open("probe/gasit.zip", "wb").write(date[i:])
    print("arhiva extrasa de la octetul", i, "din", len(date), "(fisier PNG + ZIP lipit)")
    with zipfile.ZipFile("probe/gasit.zip") as z:
        for nume in z.namelist():
            print("in arhiva:", nume, "->", z.read(nume).decode().strip())


if __name__ == "__main__":
    globals()[sys.argv[1].lower()]()
