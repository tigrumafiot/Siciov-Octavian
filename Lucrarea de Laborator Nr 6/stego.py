# B5

from PIL import Image
img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.get_flattened_data())
mesaj = b"FLAG{ascuns_in_pixeli}" + b"\x00"
biti = "".join(f"{x:08b}" for x in mesaj)
px_nou = []
index = 0

for pixel in px:
    canale = list(pixel)
    for j in range(3):
        if index < len(biti):
            canale[j] = (canale[j] & ~1) | int(biti[index])
            index += 1
    px_nou.append(tuple(canale))

img.putdata(px_nou)
img.save("stego.png")
print("Mesaj ascuns:", mesaj[:-1].decode())
print("Numar de biti ascunsi:", len(biti))
print("Imagine salvata: stego.png")

# B6

img_stego = Image.open("stego.png").convert("RGB")
px_stego = list(img_stego.get_flattened_data())
biti_extrasi = ""

for r, g, b in px_stego:
    biti_extrasi += str(r & 1)
    biti_extrasi += str(g & 1)
    biti_extrasi += str(b & 1)

mesaj_extras = bytearray()

for i in range(0, len(biti_extrasi) - 7, 8):
    octet = int(biti_extrasi[i:i + 8], 2)
    if octet == 0:
        break
    mesaj_extras.append(octet)

print("\nMesaj extras:", mesaj_extras.decode())