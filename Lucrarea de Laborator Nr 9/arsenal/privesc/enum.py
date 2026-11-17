# A1
import argparse
import json
import os
def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        return [
            linie.strip()
            for linie in f
            if linie.strip() and not linie.strip().startswith("#")
        ]

# A2
def nume(cale):
    return cale.rsplit("/", 1)[-1]

# A3
GTFO = {
    "find", "vim.basic", "vim", "nmap", "cp",
    "bash", "less", "awk", "python3", "perl"
}

def suid_constatari(cale):
    cai = citeste_linii(cale)
    constatari = []
    for c in sorted(set(cai)):
        nume_fisier = nume(c)
        constatare = {
            "cale": c,
            "nume": nume_fisier,
            "risc": "mare" if nume_fisier in GTFO else "normal"
        }
        constatari.append(constatare)
    return constatari

# A4
def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(" : ", 1)
        constatare = {
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": "mare" if "NOPASSWD" in drept else "normal"
        }
        out.append(constatare)
    return out

def cron_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        campuri = ln.split()
        if len(campuri) < 7:
            continue
        user = campuri[5]
        comanda = " ".join(campuri[6:])
        constatare = {
            "user": user,
            "comanda": comanda
        }
        out.append(constatare)
    return out

def enumereaza(d):
    return {
        "suid": suid_constatari(os.path.join(d, "suid.txt")),
        "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
        "cron": cron_constatari(os.path.join(d, "crontab.txt"))
    }

# A5
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
    utilizatori_sudo = {c["user"] for c in raport["sudo"]}
    utilizatori_cron = {c["user"] for c in raport["cron"]}
    utilizatori = utilizatori_sudo | utilizatori_cron
    print("utilizatori implicati:", ", ".join(sorted(utilizatori)))
    cale_json = os.path.join(os.path.dirname(__file__), "enum.json")
    with open(cale_json, "w", encoding="utf-8") as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    print("Raport salvat in enum.json")

if __name__ == "__main__":
    main()