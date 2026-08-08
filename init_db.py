import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

with connection:
    connection.execute('DROP TABLE IF EXISTS products')
    connection.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            image_url TEXT
        )
    ''')

produits_test = [
    ('Princesse Rousse', 'Crochet', 20.00, 'Fait main avec amour', 'static/images/IMG_20260628_140957.jpg'),
    ('Poupée à natte', 'Crochet', 20.00, 'Fait main avec amour', 'static/images/IMG_20260628_141124.jpg'),
    ('Champignon aux longues jambes', 'Crochet', 15.00, 'Fait main avec amour', 'static/images/IMG_20260628_141141.jpg'),
    ('Pouppée rouge', 'Crochet', 20.00, 'Fait main avec amour', 'static/images/IMG_20260628_141438.jpg'),
    ('Poupée rose', 'Crochet', 20.00, 'Fait main avec amour', 'static/images/IMG_20260628_141552.jpg'),
    ('Poupée bleue', 'Crochet', 20.00, 'Fait main avec amour', 'static/images/IMG_20260628_141602.jpg'),
    ('Poupée bleu foncé', 'Crochet', 20.00, 'Fait main avec amour', 'static/images/IMG_20260628_141612.jpg'),
    ('Petits poissons', 'Crochet', 15.00, 'Fait main avec amour', 'static/images/IMG_20260628_141650.jpg'),
    ('Petite tortue', 'Crochet', 12.00, 'Fait main avec amour', 'static/images/IMG_20260628_141707.jpg'),
    ('Elephant en salopette', 'Crochet', 15.00, 'Fait main avec amour', 'static/images/IMG_20260628_141852.jpg'),
    ('Ecureuil', 'Crochet', 15.00, 'Fait main avec amour', 'static/images/IMG_20260628_141907.jpg'),
    ('Poule de Pâques', 'Crochet', 15.00, 'Fait main avec amour', 'static/images/IMG_20260628_141924.jpg'),
    ('Petite poupée et son panier', 'Crochet', 10.00, 'Fait main avec amour', 'static/images/IMG_20260628_142013.jpg'),
    ('Hérisson', 'Crochet', 20.00, 'Fait main avec amour', 'static/images/IMG_20260628_143106.jpg'),
    ('Petit ourson et ses amis', 'Crochet', 30.00, 'Fait main avec amour, possibilité de vente unité', 'static/images/IMG_20260628_143218.jpg'),
    ('Petit lapin de Pâques', 'Crochet', 15.00, 'Fait main avec amour', 'static/images/IMG_20260628_143327.jpg'),
    ('Poupées soeurs', 'Crochet', 25.00, 'Fait main avec amour, possibilité de vente unité', 'static/images/IMG_20260628_143421.jpg'),
    ('Petites poupées', 'Crochet', 12.00, 'Fait main avec amour, vente unitaire', 'static/images/IMG_20260628_143524.jpg'),
    ('Petites tortues et pieuvre', 'Crochet', 8.00, 'Fait main avec amour, vente unitaire', 'static/images/IMG_20260628_143625.jpg'),
    ('Petite tortues, pieuvre et hérisson', 'Crochet', 8.00, 'Fait main avec amour, vente unitaire', 'static/images/IMG_20260628_143657.jpg'),
    ('Petites poupées', 'Crochet', 10.00, 'Fait main avec amour, vente unitaire', 'static/images/IMG_20260628_143942.jpg'),
    ('Poupée bleue, poupée rose', 'Crochet', 15.00, 'Fait main avec amour, vente unitaire', 'static/images/IMG_20260628_144359.jpg'),
    ('Poupée Betty Boop', 'Crochet', 20.00, 'Fait main avec amour', 'static/images/IMG_20260628_144410.jpg'),
    ('Lapin jaune', 'Crochet', 20.00, 'Fait main avec amour', 'static/images/IMG_20260628_144419.jpg'),
    ('Lapine violette', 'Crochet', 20.00, 'Fait main avec amour', 'static/images/IMG_20260628_144444.jpg'),
    ('Lapine mauve', 'Crochet', 20.00, 'Fait main avec amour', 'static/images/IMG_20260628_144455.jpg'),
]

cursor.executemany('''
INSERT INTO products (title, category, price, description, image_url)
VALUES (?, ?, ?, ?, ?)
''', produits_test)

connection.commit()
connection.close()

print("✅ La base de données SQL 'database.db' a été créée avec succès !")