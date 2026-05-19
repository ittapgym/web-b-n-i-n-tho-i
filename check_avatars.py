import sqlite3

conn = sqlite3.connect("d:\\peach_store\\backend\\peach_store.db")
cursor = conn.cursor()
try:
    cursor.execute("SELECT id, ho_ten, email, hinh_anh FROM nguoi_dung;")
    rows = cursor.fetchall()
    print("USER DATA IN DATABASE:")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]} | Avatar: {repr(row[3])}")
except Exception as e:
    print("Error:", e)
finally:
    conn.close()
