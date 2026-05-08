from bs4 import BeautifulSoup
import json
import os
import pandas as pd

folder = "html_pages"   # tumhara folder jahan 70 files hain
all_data = []

for file in os.listdir(folder):

    if not file.endswith(".html"):
        continue

    path = os.path.join(folder, file)

    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    scripts = soup.find_all("script", type="application/ld+json")

    for s in scripts:
        try:
            data = json.loads(s.string)

            # sirf listing wala JSON chahiye
            if isinstance(data, dict) and data.get("@type") == "ItemList":

                items = data.get("itemListElement", [])

                # kabhi nested list hoti hai
                if len(items) > 0 and isinstance(items[0], list):
                    items = items[0]

                for item in items:
                    try:
                        name = item.get("name")
                        url = item.get("url")

                        if name and url and "spid-" in url:
                            property_id = url.split("spid-")[-1]

                            all_data.append({
                                "property_name": name,
                                "property_id": property_id,
                                "link": url
                            })

                    except:
                        continue

        except:
            continue

# dataframe
df = pd.DataFrame(all_data)

# duplicates remove (important)
df.drop_duplicates(subset="property_id", inplace=True)

# save csv
df.to_csv("property_links.csv", index=False)

print("✅ DONE")
print("Total properties:", len(df))
print(df.head())