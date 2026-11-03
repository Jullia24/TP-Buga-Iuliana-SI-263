# -*- coding: utf-8 -*-
"""Rulează exercițiile A1-A6 pe rând:  python arsenal/forensics/exercitii_A.py A3"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from arsenal.forensics.decode import ghici_strat, desfa, desfa_straturi, sparge_xor, sparge_hash, citibil


def a1():
    s = "Salut"
    b = s.encode()
    print(b, b[0])                       # b'Salut' 83
    h = b.hex()
    print("hex      :", h)
    print("inapoi   :", bytes.fromhex(h))


def a2():
    for t in ["%2Fetc", "48656c6c6f", "U2FsdXQ=", "Salut!"]:
        print(f"{t!r:16} -> {ghici_strat(t)}")


def a3():
    for t in ["U2FsdXQ=", "48656c6c6f", "%2Fetc%2Fpasswd"]:
        strat, b = desfa(t)
        print(f"{t!r:20} -> {strat:7} -> {b}")


def a4():
    val = "NTM1OTU3NTk="
    straturi, b = desfa_straturi(val)
    print("exemplu din fisa:", val)
    print("  straturi:", " -> ".join(straturi), "| rezultat:", b.decode())
    sir = open("probe/mesaj.txt").read().strip()
    print("probe/mesaj.txt :", sir[:40] + "...")
    straturi, b = desfa_straturi(sir)
    print("  straturi:", " -> ".join(straturi))
    print("  clar    :", b.decode())


def a5():
    date = open("probe/xor.bin", "rb").read()
    gasite = sparge_xor(date)
    print(len(gasite), "chei dau rezultat imprimabil din 256")
    k, clar = gasite[0]
    print("cea mai buna cheie:", k, f"(0x{k:02x})")
    print("text:", clar)
    print("a doua clasata, pentru comparatie:", gasite[1][0], "->", gasite[1][1][:30] + "...")


def a6():
    tinta = open("probe/hashuri.txt").readline().strip()
    print("hash  :", tinta)
    print("lungime:", len(tinta), "-> md5")
    algo, parola = sparge_hash(tinta, "probe/wordlist.txt")
    print("gasit :", parola)


if __name__ == "__main__":
    globals()[sys.argv[1].lower()]()
