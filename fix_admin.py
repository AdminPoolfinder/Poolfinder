import pymysql

conn = pymysql.connect(
    host="switchback.proxy.rlwy.net",
    port=11250,
    user="root",
    password="chZMSyJSTXKZwUwDjlIDswhgbkgXFqOz",
    database="railway"
)

cursor = conn.cursor()

try:
    cursor.execute("""
        ALTER TABLE admin
        ADD COLUMN reset_token VARCHAR(255) NULL
    """)
    print("✅ Kolom reset_token berhasil ditambahkan.")
except Exception as e:
    print("reset_token:", e)

try:
    cursor.execute("""
        ALTER TABLE admin
        ADD COLUMN reset_token_expiry DATETIME NULL
    """)
    print("✅ Kolom reset_token_expiry berhasil ditambahkan.")
except Exception as e:
    print("reset_token_expiry:", e)

conn.commit()
cursor.close()
conn.close()

print("🎉 Selesai.")