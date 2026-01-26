
import sqlite3
import os
from datetime import datetime

DATABASE_NAME = 'queue.db'
STATUS_PENDING = 'pending'

def setup_database():
    """Tworzy bazę danych i tabelę, jeśli nie istnieją."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Tworzenie tabeli
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            status TEXT NOT NULL,
            creation_time TEXT NOT NULL,
            consumer_id TEXT
        )
    ''')
    conn.commit()
    conn.close()

# W oryginalnym producerze była funkcja get_next_id, 
# ale SQLite załatwia to automatycznie. Zostawiamy tylko add_task_to_queue.

def add_task_to_queue():
    """Dodaje nowe zadanie do kolejki w bazie SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        # Wstawienie zadania - ID jest automatyczne (PRIMARY KEY)
        cursor.execute('''
            INSERT INTO tasks (status, creation_time, consumer_id) 
            VALUES (?, ?, ?)
        ''', (STATUS_PENDING, creation_time, None))
        
        task_id = cursor.lastrowid
        conn.commit()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] ZADANIE DODANE: ID={task_id}, Status={STATUS_PENDING}")
        
    except sqlite3.Error as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] BŁĄD PRODUCERA: {e}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    setup_database() # Musi być wywołane, żeby utworzyć tabelę
    add_task_to_queue()