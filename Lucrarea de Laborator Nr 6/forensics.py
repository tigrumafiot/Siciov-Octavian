# B1

def tip_real(cale):
    with open(cale, "rb") as f:
        cap = f.read(8)
    if cap.startswith(b"%PDF"):
        return "pdf"
    if cap.startswith(b"\x89PNG"):
        return "png"
    if cap.startswith(b"\xff\xd8"):
        return "jpeg"
    if cap.startswith(b"PK\x03\x04"):
        return "zip/docx"
    return "necunoscut: " + cap.hex()

print("foto.jpg:", tip_real("probe/foto.jpg"))
print("ascuns.png:", tip_real("probe/ascuns.png"))

# B2

import re
with open("probe/ascuns.png", "rb") as f:
    date = f.read()

print("\nText gasit in fisier:")

for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())

# B3

from PIL import Image
from PIL.ExifTags import TAGS

img = Image.open("probe/foto.jpg")
exif = img.getexif()

print("\nMetadate EXIF:")

for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)

def grade_zecimale(coordonate, directie):
    grade, minute, secunde = coordonate
    rezultat = float(grade) + float(minute) / 60 + float(secunde) / 3600
    if directie in ("S", "W"):
        rezultat = -rezultat
    return rezultat

gps = exif.get_ifd(34853)

if gps:
    latitudine = grade_zecimale(gps[2], gps[1])
    longitudine = grade_zecimale(gps[4], gps[3])
    print("\nCoordonate GPS:")
    print("Latitudine:", round(latitudine, 6))
    print("Longitudine:", round(longitudine, 6))
else:
    print("Nu exista coordonate GPS.")

# B4

import zipfile
with open("probe/ascuns.png", "rb") as f:
    date = f.read()

i = date.find(b"PK\x03\x04")

if i != -1:
    with open("gasit.zip", "wb") as f:
        f.write(date[i:])
    print("\nArhiva extrasa de la octetul:", i)
    with zipfile.ZipFile("gasit.zip", "r") as z:
        print("Fisiere in arhiva:", z.namelist())
        z.extractall("probe/extras")
        for nume in z.namelist():
            print("Continut:", z.read(nume).decode())
else:
    print("Nu a fost gasita o arhiva ZIP.")