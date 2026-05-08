from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import os, time, random

# ===== CONFIG =====
input_csv = r"property_links.csv"
save_folder = "property_html"
os.makedirs(save_folder, exist_ok=True)

START = 1381
END =   1570 # first batch

df = pd.read_csv(input_csv)

# ===== DRIVER FUNCTION =====
def start_driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 25)

    # warmup
    driver.get("https://www.99acres.com")
    time.sleep(5)

    return driver, wait

driver, wait = start_driver()

# ===== HELPERS =====
def is_blocked(html):
    h = html.lower()
    return "captcha" in h or "access denied" in h or "are you a bot" in h

def slow_scroll():
    last = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, 700);")
        time.sleep(random.uniform(1.5, 2.5))
        new = driver.execute_script("return document.body.scrollHeight")
        if new == last:
            break
        last = new

# ===== MAIN LOOP =====
for i in range(START, END):

    row = df.iloc[i]

    link = row["link"]
    pid = str(row["property_id"])

    file_path = os.path.join(save_folder, f"{pid}.html")

    if os.path.exists(file_path):
        print(f"⏭ Skip: {pid}")
        continue

    print(f"\n🔵 [{i}] Opening: {pid}")

    try:
        driver.get(link)

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        time.sleep(4)

        slow_scroll()
        time.sleep(4)

        html = driver.page_source

        if is_blocked(html):
            print("⚠️ BLOCKED → skip and continue")
            continue

        if "pd__contentWrap" not in html:
            print("⚠️ Incomplete → skip")
            continue

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"✅ Saved: {pid}")

    except Exception as e:
        print("❌ Error:", e)

    # ===== HUMAN DELAY =====
    time.sleep(random.uniform(5, 10))

    # ===== RESTART DRIVER =====
    if i % 30 == 0 and i != START:
        print("♻️ Restarting browser...")
        driver.quit()
        time.sleep(10)
        driver, wait = start_driver()

    # ===== LONG BREAK =====
    if i % 50 == 0 and i != START:
        print("😴 Long break...")
        time.sleep(random.uniform(60, 120))

driver.quit()

print("\n🎉 DONE BATCH 600–900")