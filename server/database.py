import sqlite3
import os

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'reconflow.db')
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS assets 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  target_domain TEXT, 
                  asset_value TEXT UNIQUE, 
                  status TEXT, 
                  assigned_to TEXT, 
                  date_added DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    c.execute('''CREATE TABLE IF NOT EXISTS activity_logs 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user TEXT, 
                  action TEXT, 
                  asset TEXT, 
                  time DATETIME DEFAULT CURRENT_TIMESTAMP)''')

    conn.commit()
    conn.close()
    print("[+] Database Initialized Successfully! The Brain is ready 🧠")

if __name__ == '__main__':
    init_db()
