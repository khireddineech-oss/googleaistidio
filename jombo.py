import sqlite3, os, time, glob

print("[*] Searching for database...")
db_files = glob.glob("/data/data/com.google.android.gms/databases/games*.db")

if not db_files:
    print("[-] Database not found!")
    exit()

db_path = db_files[0]
print(f"[+] Found: {db_path}")

# نسخ القاعدة لمسار يسمح بالقراءة
os.system(f"tsu -c 'cp {db_path} /sdcard/games_temp.db'")
os.system(f"tsu -c 'chmod 666 /sdcard/games_temp.db'")

# ضع معرفات الإنجازات هنا (مفصولة بفاصلة)
ACHIEVEMENTS = ["CgkI7rC1wLwbEAIQBw"]

conn = sqlite3.connect("/sdcard/games_temp.db")
cur = conn.cursor()
now = int(time.time() * 1000)

cur.execute("SELECT external_player_id FROM achievement_instances LIMIT 1")
row = cur.fetchone()
player_id = row[0] if row else ""

cur.execute("SELECT context_client_id FROM client_contexts LIMIT 1")
row = cur.fetchone()
context_id = row[0] if row else ""

for ach in ACHIEVEMENTS:
    try:
        cur.execute("""
            INSERT INTO achievement_pending_ops 
            (external_player_id, external_achievement_id, context_client_id, op_type, state, timestamp)
            VALUES (?, ?, ?, 0, 0, ?)
        """, (player_id, ach, context_id, now))
        print(f"[+] Sync added for: {ach}")
    except Exception as e:
        print(f"[-] Error: {e}")

conn.commit()
conn.close()

# إعادة القاعدة وتشغيل Play Games
os.system(f"tsu -c 'cp /sdcard/games_temp.db {db_path}'")
os.system("tsu -c 'am force-stop com.google.android.gms'")
time.sleep(2)
os.system("tsu -c 'monkey -p com.google.android.play.games -c android.intent.category.LAUNCHER 1'")

print("[✓] Done. Open Play Games.")
