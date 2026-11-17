# Partea 8

from httptools import PATHS, report
def main():
    rezultate = []
    for path in PATHS:
        rezultat = report(path)
        rezultat["path"] = path
        rezultate.append(rezultat)
    reusite = [
        r for r in rezultate
        if r["status"] == 200
    ]
    reusite.sort(
        key=lambda r: r["seconds"],
        reverse=True
    )
    print("\nRaport HTTP:")
    for r in reusite:
        print(
            f'{r["path"]} -> {r["status"]}, '
            f'{r["seconds"]:.2f} secunde'
        )
    esuate = len(rezultate) - len(reusite)
    print(f"Reusite: {len(reusite)} | Esuate: {esuate}")

if __name__ == "__main__":
    main()

