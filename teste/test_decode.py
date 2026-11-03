# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arsenal.forensics.decode import (ghici_strat, desfa, desfa_straturi,
                                      sparge_xor, sparge_hash)


def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"


def test_hex():
    strat, b = desfa("48656c6c6f")
    assert strat == "hex"
    assert b == b"Hello"


def test_url():
    strat, b = desfa("%2Fetc%2Fpasswd")
    assert strat == "url"
    assert b == b"/etc/passwd"


def test_ordinea_straturilor():
    assert ghici_strat("%2Fetc") == "url"
    assert ghici_strat("48656c6c6f") == "hex"
    assert ghici_strat("Salut!") == "necunoscut"


def test_straturi_multiple():
    sir = open("probe/mesaj.txt").read().strip()
    straturi, b = desfa_straturi(sir)
    assert straturi == ["base64", "base64", "hex"]
    assert b == b"FLAG{straturi_de_encoding}"


def test_xor_cheia_buna_prima():
    k, clar = sparge_xor(open("probe/xor.bin", "rb").read())[0]
    assert k == 0x80
    assert "FLAG{xor_un_octet}" in clar


def test_hash_dictionar():
    algo, parola = sparge_hash("5f4dcc3b5aa765d61d8327deb882cf99", "probe/wordlist.txt")
    assert (algo, parola) == ("md5", "password")


if __name__ == "__main__":      # ruleaza fara pytest:  python teste/test_decode.py
    trecute = 0
    teste = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    for nume, f in teste:
        f()
        trecute += 1
        print(f"PASSED  {nume}")
    print(f"\n{trecute} din {len(teste)} teste au trecut")
