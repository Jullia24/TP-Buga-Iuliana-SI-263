# Tehnici de programare — Buga Iuliana, SI-263 (UTM, FCIM)

## Laboratoare

| Laborator | Unde se află codul |
|---|---|
| Lab 6 — Informații invizibile: forensics și steganografie | `arsenal/forensics/` (Lucrarea A: decoder), `forensics.py`, `stego.py`, `challenge.py` (Lucrarea B), `teste/`, `probe/`, `stego.png` |
| Laborator Python — funcții, metode și importuri pe web | `web_lab/` (`webtools.py`, `main.py`, `report.csv`, `report.json`) |

## Rapoarte

Rapoartele de laborator (L1, L2, L4, L5, L6) sunt în folderul `rapoarte/`.

## Cum rulezi

**Lab 6**, din rădăcina depozitului:

    pip install pillow
    python probe/pregateste.py
    python arsenal/forensics/decode.py "NTM1OTU3NTk="
    python -m pytest teste/

**Laboratorul Python web:**

    pip install requests
    cd web_lab
    python main.py https://cybercor.org
