from bs4 import BeautifulSoup
import pandas as pd
import os, json, re

folder = r"Data Gathering/gurgaon_property_html"

data = []

files = [f for f in os.listdir(folder) if f.endswith(".html")]
print(f"🚀 Total files: {len(files)}")

for idx, file in enumerate(files, start=1):

    file_path = os.path.join(folder, file)
    property_id = file.replace(".html", "")

    print(f"\n🔵 {idx}/{len(files)} → {property_id}")

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # =========================
    # JSON DATA
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

    property_name = json_data.get("name", "")
    description = json_data.get("description", "")
    link = json_data.get("url", "")
    bedRoom = json_data.get("numberOfRooms", "")
    bathroom = json_data.get("numberOfBathroomsTotal", "")
    floorNum = json_data.get("floorLevel", "")
    areaWithType = ""
    area_block = soup.select_one("#factArea")
    if area_block:
        areaWithType = area_block.text.strip()

    address_json = json_data.get("address", {})
    society = address_json.get("name", "")
    address = address_json.get("streetAddress", "")
    locality = address_json.get("addressLocality", "")

    geo = json_data.get("geo", {})
    lat = geo.get("latitude", "")
    lng = geo.get("longitude", "")

    # =========================
    # PRICE
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
    # TABLE DATA (MULTI METHOD)
    # =========================
    table_data = {}

    # METHOD 1 → tableRow
    rows = soup.select("div.component__tableRow")
    for row in rows:
        try:
            key = row.select_one("div.component__tableHead").text.strip()
            value = row.select_one("div.component__details").text.strip()
            table_data[key] = value
        except:
            continue

    # METHOD 2 → listItem
    if not table_data:
        rows = soup.select("li.component__listItem")
        for row in rows:
            try:
                key = row.select_one("span.component__label").text.strip()
                value = row.select_one("span.component__value").text.strip()
                table_data[key] = value
            except:
                continue

    # METHOD 3 → fallback
    if not table_data:
        for div in soup.find_all("div"):
            try:
                label = div.get("data-label")
                if label:
                    table_data[label] = div.text.strip()
            except:
                continue

    # DEBUG (optional)
    # print(table_data)

    # =========================
    # MAP FIELDS
    # ===== DIRECT EXTRACTION (CRITICAL FIX) =====

    # Facing
    facing_tag = soup.select_one("#facingLabel")
    if facing_tag:
        facing = facing_tag.text.strip()

    # Age / Possession
    age_tag = soup.select_one("#agePossessionLbl")
    if age_tag:
        agePossession = age_tag.text.strip()

    # Balcony
    balcony_tag = soup.select_one("#balconyNum")
    if balcony_tag:
        balcony = balcony_tag.text.strip()

    # Additional Rooms
    add_room_tag = soup.select_one("#additionalRooms")
    if add_room_tag:
        additionalRoom = add_room_tag.text.strip()

    floorNum = table_data.get("Floor", floorNum)

    if "Built-up area" in table_data:
        areaWithType = table_data.get("Built-up area")
    elif "Super Built-up area" in table_data:
        areaWithType = table_data.get("Super Built-up area")

    # =========================
    # AREA
    # =========================
    area = ""
    if areaWithType:
        match = re.search(r"\d+", areaWithType)
        if match:
            area = match.group()

    # =========================
    # NEARBY
    # =========================
    nearbyLocations = []

    for item in soup.select(".NearByLocation__infoText"):
        text = item.text.strip()
        if text:
            nearbyLocations.append(text)

    # =========================
    # FEATURES
    # =========================
    features = []

    blocks = soup.select("div[data-label='FACILITIES']")

    for block in blocks:
        for li in block.select("li"):
            text = li.get_text(strip=True)
            if text:
                features.append(text)

    # remove duplicates
    features = list(dict.fromkeys(features))

    furnishDetails = []

    furnish_block = soup.select("div[data-label='FURNISHING'] li")

    for li in furnish_block:
        text = li.get_text(strip=True)
        if text:
            furnishDetails.append(text)

    # =========================
    # RATING
    # =========================
    rating = []

    blocks = soup.select(".ratingByFeature__contWrap")

    for b in blocks:
        try:
            name = b.select_one(".list_header_semiBold").text.strip()
            value = b.select_one(".caption_subdued_medium").text.strip()
            rating.append(f"{name}: {value}")
        except:
            continue

    # =========================
    # PRICE PER SQFT
    # =========================
    price_per_sqft = ""

    price_span = soup.select_one("#pdPrice2")

    if price_span:
        parent_div = price_span.find_parent("div")

        if parent_div:
            full_text = parent_div.get_text(" ", strip=True)

            print("DEBUG TEXT:", full_text)  # 🔥 important

            import re
            match = re.search(r'@\s*([\d,]+)\s*per\s*sqft', full_text)

            if match:
                price_per_sqft = match.group(1)
    # =========================
    # FINAL DATA
    # =========================
    property_data = {
        'property_name': property_name,
        'link': link,
        'society': society,
        'price': price,
        'area': area,
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
        'price_per_sqft': price_per_sqft
    }

    data.append(property_data)

    print(f"✅ Extracted | Total rows: {len(data)}")

    # SAVE EVERY 50
    if len(data) % 50 == 0:
        pd.DataFrame(data).to_csv("gurgaon_final.csv", index=False)
        print("💾 Auto saved")

# FINAL SAVE
df = pd.DataFrame(data)
df.to_csv("gurgaon_final.csv", index=False)

print("\n🎉 DONE — FULL DATASET READY")
print("📊 Total rows:", len(df))