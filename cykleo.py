from requests import Session, codes

print("debut")
emplacements = ["gare", "place de", "palais"]
URL = "https://portail.cykleo.fr/pu/stations/availability?organization_id=5"
with Session() as s:
    s.headers['Referer'] = 'https://portail.cykleo.fr/TAO_velos/carte_stations'

    p1 = s.get(URL, timeout=(4, 10))
    print(p1)
    print(p1.headers)
    if "json" not in p1.headers['Content-Type'].lower() or p1.status_code != codes["OK"]:
        print("fin")
        exit(0)

    print(p1.json())
    for station in p1.json():
        trouve = False
        for place in emplacements:
            if place.lower() in station["station"]["assetStation"]["commercialName"].lower():
                trouve = True
                break
        if trouve:
            ligne = station["station"]["assetStation"]["commercialName"].ljust(25)[:25]
            ligne += ", " + "Dock:" + str(station["availableDockCount"]).rjust(2)
            ligne += ", " + "Classic:" + str(station["availableClassicBikeCount"]).rjust(2)
            ligne += ", " + "Electric:" + str(station["availableElectricBikeCount"]).rjust(2)
            ligne += (" " + station["station"]["status"]) if station["station"]["status"] != "IN_SERVICE" else " (AVAIL)"
            print(ligne)
