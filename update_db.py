import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE products ADD COLUMN stock INTEGER DEFAULT 1;")
    print("Colonne 'stock' ajoutée avec succès !")
except sqlite3.OperationalError:
    print("ℹ️ La colonne 'stock' existe déjà.")

    cursor.execute("UPDATE products SET stock = 2 WHERE id = 22;")
    cursor.execute("UPDATE products SET stock = 2 WHERE id = 21;")
    cursor.execute("UPDATE products SET stock = 5 WHERE id = 20;")
    cursor.execute("UPDATE products SET stock = 3 WHERE id = 19;")
    cursor.execute("UPDATE products SET stock = 4 WHERE id = 18;")
    cursor.execute("UPDATE products SET stock = 2 WHERE id = 17;")
    cursor.execute("UPDATE products SET stock = 2 WHERE id = 8;")

conn.commit()
conn.close()