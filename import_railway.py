import mysql.connector

conn = mysql.connector.connect(
    host="switchback.proxy.rlwy.net",
    port=11250,
    user="root",
    password="chZMSyJSTXKZwUwDjlIDswhgbkgXFqOz",
    database="railway"
)

cursor = conn.cursor()

with open("poolfinder_db.sql", "r", encoding="utf-8") as f:
    sql = f.read()

for statement in sql.split(";"):
    statement = statement.strip()
    if statement:
        try:
            cursor.execute(statement)
        except Exception as e:
            print("Error:", e)

conn.commit()
cursor.close()
conn.close()

print("✅ Import selesai!")