
import sqlite3
from sqlite3 import Error
conn = sqlite3.connect('product/electric/laptop/product.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS products(
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    price INTEGER NOT NULL,
                    discription  TEXT NOT NULL,
                    title TEXT NOT NULL,
                    type TEXT NOT NULL,
                    ram TEXT NOT NULL,
                    C_type TEXT NOT NULL,
                    O_detail TEXT NOT NULL,
                    processer TEXT NOT NULL,
                    n_sell INTEGER,
                    reviews INTEGER,
                    image TEXT
               );''')   
conn.commit()
conn.close()
