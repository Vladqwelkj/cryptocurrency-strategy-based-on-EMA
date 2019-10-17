import config
import sqlite3
 
conn = sqlite3.connect(config.DB_NAME) # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
 
# Создание таблицы
cursor.execute("drop table trades")
cursor.execute("drop table balance")

cursor.execute("""CREATE TABLE balance
                  (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                  value DOUBLE NOT NULL)
               """)


cursor.execute("""CREATE TABLE trades
                  (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
                  is_long boolean NOT NULL,
                  enter_original float NOT NULL,
                  enter_fact float,
                  targets text, 
                  stop_price text NOT NULL,
                  is_stop_triggered boolean DEFAULT 0,
                  qty INTEGER NOT NULL)
               """)

#json massive [{order_id, is_filled, qty}, ...] -targets