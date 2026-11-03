# -*- coding: utf-8 -*-
"""Lucrarea B (B5-B6): steganografie LSB.
Rulare:  python stego.py ascunde   |   python stego.py dezvaluie"""
import sys
import warnings
from PIL import Image

warnings.filterwarnings("ignore", category=DeprecationWarning)   # getdata() e marcat invechit in Pillow nou

MESAJ = b"FLAG{ascuns_in_pixeli}"


def ascunde(sursa="probe/foto.jpg", iesire="stego.png", mesaj=MESAJ):
    img = Image.open(sursa).convert("RGB")
    px = list(img.getdata())
    biti = "".join(f"{x:08b}" for x in mesaj + b"\x00")     # \x00 = sfarsit de mesaj
    if len(biti) > len(px) * 3:
        raise ValueError("mesajul nu incape in imagine")
    nou, i = [], 0
    for (r, g, b) in px:
        canale = [r, g, b]
        for c in range(3):
            if i < len(biti):
                canale[c] = (canale[c] & ~1) | int(biti[i])
                i += 1
        nou.append(tuple(canale))
    img.putdata(nou)
    img.save(iesire)                       # PNG = fara pierdere
    return len(biti)


def dezvaluie(cale="stego.png"):
    px = list(Image.open(cale).convert("RGB").getdata())
    biti = ""
    for (r, g, b) in px:
        biti += f"{r & 1}{g & 1}{b & 1}"
    octeti = bytearray()
    for i in range(0, len(biti) - 7, 8):
        o = int(biti[i:i + 8], 2)
        if o == 0:                          # primul octet 0 = final de mesaj
            break
        octeti.append(o)
    return octeti.decode(errors="replace")


def compara(a="probe/foto.jpg", b="stego.png"):
    pa = list(Image.open(a).convert("RGB").getdata())
    pb = list(Image.open(b).convert("RGB").getdata())
    dif = [max(abs(x - y) for x, y in zip(p, q)) for p, q in zip(pa, pb)]
    return sum(1 for d in dif if d), max(dif), len(pa)


if __name__ == "__main__":
    if sys.argv[1] == "ascunde":
        n = ascunde()
        print(f"am scris {n} biti ({n // 8} octeti, cu terminator) in stego.png")
        schimbati, maxim, total = compara()
        print(f"pixeli modificati: {schimbati} din {total}; diferenta maxima pe un canal: {maxim}")
    elif sys.argv[1] == "dezvaluie":
        print("mesaj dezvaluit:", dezvaluie())
