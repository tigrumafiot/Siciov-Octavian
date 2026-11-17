# A1 + A2
from dataclasses import dataclass, asdict
import json

CAI_SUSPECTE = ("\\Temp\\", "\\Roaming\\")

@dataclass
class Proces:
    pid: int; nume: str; user: str; cale: str
    def e_suspect(self):
        for folder in CAI_SUSPECTE:
            if folder in self.cale:
                return True
        return False

# A3
SUSPECTE_ID = {4625, 1102, 7045}

@dataclass
class Eveniment:
    id: int; nivel: str; sursa: str; cont: str; mesaj: str
    def e_suspect(self):
        if self.id in SUSPECTE_ID or self.nivel == "critical":
            return True
        else:
            return False

# A4
def procese_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Proces(**d) for d in json.load(f)]

# B1 + B2
@dataclass
class Inventar:
    procese: list
    @classmethod
    def din_json(cls, cale):
        with open(cale, encoding="utf-8") as f:
            return cls([Proces(**d) for d in json.load(f)])
    def __len__(self):
        return len(self.procese)
    def suspecte(self):
        return [p for p in self.procese if p.e_suspect()]
    def pe_user(self):
        rezultat = {}
        for p in self.procese:
            rezultat.setdefault(p.user, []).append(p.nume)
        return rezultat

# B3
def evenimente_din_json(cale):
    with open(cale, encoding="utf-8") as f:
        return [Eveniment(**d) for d in json.load(f)]

def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    inv = Inventar.din_json(a.capturi + "/procese.json")
    ev = evenimente_din_json(a.capturi + "/evenimente.json")
    suspecte = inv.suspecte()
    alarma = [e for e in ev if e.e_suspect()]
    if a.json:
        raport = {
            "procese_suspecte": [asdict(p) for p in suspecte],
            "evenimente_alarma": [asdict(e) for e in alarma]
        }
        print(json.dumps(raport, indent=2, ensure_ascii=False))
    else:
        print(f"Procese: {len(inv)} | suspecte: {len(suspecte)}")
        for p in suspecte:
            print(f"  [{p.pid}] {p.nume}  ({p.user})  {p.cale}")
        print(f"Evenimente: {len(ev)} | alarma: {len(alarma)}")
        for e in alarma:
            print(f"  {e.id} [{e.nivel}] {e.cont}: {e.mesaj}")

if __name__ == "__main__":
    main()