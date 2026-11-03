# -*- coding: utf-8 -*-
"""Varful salii: challenge.bin = base64 peste XOR cu cheie de un octet. Rulare: python challenge.py"""
import base64
import hashlib

brut = open("probe/challenge.bin", "rb").read()
print("1) incepe ca:", brut[:24], "-> alfabet base64 -> strat base64")
xored = base64.b64decode(brut)
print("2) dupa base64:", xored.hex(" "), "(neimprimabil -> XOR)")

hint = open("probe/challenge_hint.txt").read()
md5_asteptat = hint.split("=")[-1].strip()
for k in range(256):
    clar = bytes(b ^ k for b in xored)
    if all(32 <= c < 127 for c in clar) and hashlib.md5(clar).hexdigest() == md5_asteptat:
        print(f"3) cheie XOR: {k} (0x{k:02x})")
        print("4) text clar :", clar.decode())
        print("5) md5(clar) :", hashlib.md5(clar).hexdigest(), "== hint  -> VERIFICAT")
