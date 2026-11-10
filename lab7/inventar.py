import json
import argparse

def citeste_tinte(cale):
    with open(cale, 'r') as f:
        data = json.load(f)
    return data["tinte"]

def proceseaza(tinte, prag):
    rezultat = []
    print(f"Tinte citite: {len(tinte)}")
    
    # Greșeală: nume greșit de variabilă (NameError)
    for t in tinte:
        port_str = t.get("port")
        try:
            port = int(port_str)
        except ValueError:
            print(f"sar peste {t['ip']} : port invalid {port_str}")
            continue
            
        # Greșeală: concatenare de tip invalid (TypeError)
        serviciu = t["serviciu"] + ": " + str(port)
        
        if port > prag:
            rezultat.append(t["ip"])
            
    return rezultat

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fisier")
    parser.add_argument("--prag", type=int, default=1024)
    args = parser.parse_args()
    
    tinte = citeste_tinte(args.fisier)
    peste = proceseaza(tinte, args.prag)
    print(f"Peste {args.prag}: {peste}")

if __name__ == "__main__":
    main()
