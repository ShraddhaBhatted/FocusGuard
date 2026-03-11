import sqlite3
import pandas as pd
import os
import shutil
from urllib.parse import urlparse

print("HELLO FROM CHROME SCRIPT")
input("Script reached end. Press Enter to exit...")


base_path = os.path.expanduser(
    r"C:\Users\ASUS\AppData\Local\Google\Chrome\User Data\Profile 1"
)

profile_path = None
for folder in os.listdir(base_path):
    candidate = os.path.join(base_path, folder, "History")
    if os.path.exists(candidate):
        profile_path = candidate
        break

if profile_path is None:
    print("Chrome History file not found.")
    exit()

temp_copy = "History_copy"
shutil.copyfile(profile_path, temp_copy)

conn = sqlite3.connect(temp_copy)
query = """
SELECT url, visit_count
FROM urls
ORDER BY last_visit_time DESC
LIMIT 50
"""
df = pd.read_sql(query, conn)
conn.close()
os.remove(temp_copy)

def extract_domain(url):
    try:
        return urlparse(url).netloc
    except:
        return None

df["site"] = df["url"].apply(extract_domain)
df["time_spent"] = df["visit_count"] * 2
df["label"] = "unknown"

df = df[["site", "time_spent", "label"]]
df.dropna(inplace=True)

existing = pd.read_csv("browsing_data.csv")
combined = pd.concat([existing, df]).drop_duplicates(subset=["site"])
combined.to_csv("browsing_data.csv", index=False)

print("Chrome history successfully added to CSV!")

