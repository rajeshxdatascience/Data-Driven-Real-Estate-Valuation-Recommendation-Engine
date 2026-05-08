from bs4 import BeautifulSoup
import pandas as pd
import os, json

folder = r"Data Gathering\gurgaon_property_html"

data = []

files = [f for f in os.listdir(folder) if f.endswith(".html")]
print(f"Total files: {len(files)}")

for idx, file in enumerate(files, start=1):

    file_path = os.path.join(folder, file)
    property_id = file.replace(".html", "")

    print(f"\n🔵 {idx} → {property_id}")

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # =========================
    # JSON (PRIMARY SOURCE)
    # =========================
    json_data = {}

    for script in soup.find_all("script", type="application/ld+json"):
        try:
            temp = json.loads(script.string)
            if isinstance(temp, dict) and temp.get("@type") in ["Apartment", "Product"]:
                json_data = temp
                break
        except:
            continue

    # =========================
    # BASIC (JSON)
    # =========================
    property_name = json_data.get("name", "")
    description = json_data.get("description", "")
    link = json_data.get("url", "")

    bedRoom = json_data.get("numberOfRooms", "")
    bathroom = json_data.get("numberOfBathroomsTotal", "")
    floorNum = json_data.get("floorLevel", "")
    areaWithType = json_data.get("floorSize", "")

    # =========================
    # ADDRESS
    # =========================
    address_json = json_data.get("address", {})
    society = address_json.get("name", "")
    address = address_json.get("streetAddress", "")
    locality = address_json.get("addressLocality", "")

    # =========================
    # GEO
    # =========================
    geo = json_data.get("geo", {})
    lat = geo.get("latitude", "")
    lng = geo.get("longitude", "")

    # =========================
    # PRICE (MULTIPLE LOCATIONS)
    # =========================
    price = ""

    p = soup.select_one("div.component__pdPropValue")
    if p:
        price = p.text.strip()

    if not price:
        p = soup.find("span", id="pdPrice2")
        if p:
            price = p.text.strip()

    # =========================
    # TABLE DATA (MAIN GOLD)
    # =========================
    table_data = {}

    rows = soup.select("div.pd__contentWrap div")

    for row in rows:
        try:
            key = row.select_one("div:first-child").text.strip()
            value = row.select_one("div:last-child").text.strip()
            table_data[key] = value
        except:
            continue

    balcony = table_data.get("Balcony", "")
    additionalRoom = table_data.get("Additional Rooms", "")
    facing = table_data.get("Facing", "")
    agePossession = table_data.get("Age of Property", "")
    floorNum = table_data.get("Floor", floorNum)

    # =========================
    # NEARBY
    # =========================
    nearbyLocations = [x.text.strip() for x in soup.select(".Nearby__item")]

    # =========================
    # FEATURES / FURNISHING
    # =========================
    furnishDetails = []
    features = []

    for li in soup.find_all("li"):
        text = li.text.strip()
        if text:
            features.append(text)

        if any(k in text for k in ["AC", "Bed", "Wardrobe", "Geyser"]):
            furnishDetails.append(text)

    # =========================
    # RATING
    # =========================
    rating = [r.text.strip() for r in soup.select(".rating__wrap")]

    # =========================
    # FINAL RAW DATA
    # =========================
    property_data = {
        'property_name': property_name,
        'link': link,
        'society': society,
        'price': price,
        'area': "",
        'areaWithType': areaWithType,
        'bedRoom': bedRoom,
        'bathroom': bathroom,
        'balcony': balcony,
        'additionalRoom': additionalRoom,
        'address': address,
        'floorNum': floorNum,
        'facing': facing,
        'agePossession': agePossession,
        'nearbyLocations': nearbyLocations,
        'description': description,
        'furnishDetails': furnishDetails,
        'features': features,
        'rating': rating,
        'property_id': property_id,
        'latitude': lat,
        'longitude': lng,
        'locality': locality,
        'price_per_sqft': "",
        'city': 'gurgaon'
    }

    data.append(property_data)

    print(f"✅ Done | Total: {len(data)}")

    # safety save
    if len(data) % 50 == 0:
        pd.DataFrame(data).to_csv("gurgaon_raw.csv", index=False)
        print("💾 Auto saved")

# final save
df = pd.DataFrame(data)
df.to_csv("gurgaon_raw.csv", index=False)

print("\n🎉 DONE — RAW DATA EXTRACTED")
print("Total rows:", len(df))