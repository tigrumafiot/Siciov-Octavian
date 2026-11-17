# A1

s = "Salut"
b = s.encode()
print(b, b[0])

print(b.hex())
b_refacut = bytes.fromhex(b.hex())
print(b_refacut)

# A2

import re
def ghici_strat(s):
    if re.search(r"%[0-9a-fA-F]{2}", s):
        return "url"
    if re.fullmatch(r"[0-9a-fA-F]+", s) and len(s) % 2 == 0:
        return "hex"
    if re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"
    return "necunoscut"

print(ghici_strat("%2Fetc"))
print(ghici_strat("48656c6c6f"))
print(ghici_strat("U2FsdXQ="))
print(ghici_strat("Salut!"))

# A3

import base64
from urllib.parse import unquote
def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64":
        return strat, base64.b64decode(s)
    if strat == "hex":
        return strat, bytes.fromhex(s)
    if strat == "url":
        return strat, unquote(s).encode()
    return strat, s.encode()

print(desfa("%2Fetc"))
print(desfa("48656c6c6f"))
print(desfa("U2FsdXQ="))

# A4

def citibil(b):
    return all(32 <= c < 127 for c in b)

with open("probe/mesaj.txt", "r") as f:
    val = f.read().strip()

for i in range(8):
    strat = ghici_strat(val)
    if strat == "necunoscut":
        print("Mesaj final:", val)
        break
    strat, b = desfa(val)
    print("Pasul", i + 1, "-", strat, ":", b)
    if not citibil(b):
        print("Rezultatul nu este text citibil")
        break
    val = b.decode()

# A5

with open("probe/xor.bin", "rb") as f:
    date = f.read()

for k in range(256):
    clar = bytes(b ^ k for b in date)
    if citibil(clar) and b"FLAG{" in clar:
        print("Cheie:", k)
        print("Mesaj:", clar.decode())
        break

# A6

import hashlib
with open("probe/hashuri.txt", "r") as f:
    tinta = f.readline().strip()
print("Lungimea hash-ului:", len(tinta))

if len(tinta) == 32:
    algoritm = "md5"
elif len(tinta) == 40:
    algoritm = "sha1"
elif len(tinta) == 64:
    algoritm = "sha256"
else:
    algoritm = "necunoscut"

print("Algoritm:", algoritm)

if algoritm != "necunoscut":
    with open("probe/wordlist.txt", "r", encoding="latin1") as f:
        for cuv in f:
            cuv = cuv.strip()
            hash_calculat = hashlib.new(
                algoritm, cuv.encode()
            ).hexdigest()
            if hash_calculat == tinta:
                print("Parola gasita:", cuv)
                break

# A7

import argparse
import json

def ruleaza_a7():
    p = argparse.ArgumentParser()
    p.add_argument("intrare")
    p.add_argument("--fisier", action="store_true")
    a = p.parse_args()
    if a.fisier:
        with open(a.intrare, "rb") as f:
            date = f.read()
        mesaj = date.decode("utf-8").strip()
    else:
        mesaj = a.intrare
    strat, rezultat = desfa(mesaj)
    fisa = {
        "strat": strat,
        "rezultat": rezultat.decode("utf-8", errors="replace")
    }
    with open("arsenal/forensics/fisa.json", "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=4, ensure_ascii=False)
    print("Strat:", strat)
    print("Rezultat:", fisa["rezultat"])
    print("Fisier JSON salvat.")

if __name__ == "__main__":
    ruleaza_a7()