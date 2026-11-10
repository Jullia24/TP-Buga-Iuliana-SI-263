from arsenal.lab8.enumerare import citeste_linii, nume, GTFO

def cai(fisier):
    return set(citeste_linii(fisier))

baza = cai("arsenal/lab8/start/baza_suid.txt")
acum = cai("arsenal/lab8/start/suid.txt")
print(f"baza: {len(baza)}  acum: {len(acum)}")

noi = acum - baza
print(len(noi), "SUID noi fata de sistemul curat")
for c in sorted(noi):
    print(" ", c)

risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
print("periculoase NOI:", periculoase)