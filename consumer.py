# consumer.py (zmodyfikowany dla SQLite)

import sqlite3
import time
import uuid
from datetime import datetime

DATABASE_NAME = 'queue.db'
STATUS_PENDING = 'pending'
STATUS_IN_PROGRESS = 'in_progress'
STATUS_DONE = 'done'
TASK_DURATION_S = 30
CHECK_INTERVAL_S = 5

# Unikalny identyfikator tego konsumera
CONSUMER_ID = str(uuid.uuid4())[:8]

def setup_database():
    """Tworzy tabelę, jeśli nie istnieje (dla pewności)."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
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


def try_to_claim_task():
    """
    Próbuje atomowo zająć zadanie 'pending' zmieniając status na 'in_progress'.
    Używa transakcji, aby zapobiec jednoczesnemu przejęciu przez wielu konsumerów.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    task_id = None
    
    try:
        # Zaczynamy transakcję blokującą dostęp do bazy
        conn.isolation_level = 'EXCLUSIVE' 
        cursor.execute('BEGIN EXCLUSIVE') 
        
        # 1. Znajdujemy najstarsze zadanie ze statusem 'pending'
        cursor.execute('''
            SELECT id FROM tasks 
            WHERE status = ? 
            ORDER BY creation_time ASC 
            LIMIT 1
        ''', (STATUS_PENDING,))
        
        row = cursor.fetchone()
        
        if row:
            task_id = row[0]
            
            # 2. Aktualizujemy status zadania w tej samej transakcji
            cursor.execute('''
                UPDATE tasks 
                SET status = ?, consumer_id = ? 
                WHERE id = ?
            ''', (STATUS_IN_PROGRESS, CONSUMER_ID, task_id))
            
            # Zatwierdzamy, uwalniając blokadę.
            conn.commit()
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Konsumer {CONSUMER_ID}: POBRANO zadanie ID={task_id}. Status -> {STATUS_IN_PROGRESS}")
            
        else:
            conn.commit() # Zwalnia blokadę, nawet jeśli nic nie znaleziono
            
    except sqlite3.Error as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Konsumer {CONSUMER_ID}: BŁĄD przejęcia zadania: {e}")
        conn.rollback()
        task_id = None
        
    finally:
        conn.close()
        return task_id

def finish_task(task_id):
    """Zmienia status zadania na 'done'."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE tasks 
            SET status = ? 
            WHERE id = ? AND consumer_id = ?
        ''', (STATUS_DONE, task_id, CONSUMER_ID))
        
        conn.commit()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Konsumer {CONSUMER_ID}: ZAKOŃCZONO zadanie ID={task_id}. Status -> {STATUS_DONE}")
        
    except sqlite3.Error as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Konsumer {CONSUMER_ID}: BŁĄD zakończenia zadania: {e}")
        
    finally:
        conn.close()


def run_consumer():
    # Oryginalny consumer miał while True, który otaczał całą logikę
    print(f"Konsumer {CONSUMER_ID} uruchomiony. Sprawdzanie co {CHECK_INTERVAL_S}s.")
    
    setup_database() # Upewnienie się, że jest gdzie pisać

    while True:
        task_id = try_to_claim_task()
        
        if task_id:
            # Wykonanie pracy (30s sleep) - TO JEST OSTATNIA CZĘŚĆ LOGIKI Z PLIKÓW
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Konsumer {CONSUMER_ID}: START PRACY nad zadaniem ID={task_id}. Czas: {TASK_DURATION_S}s.")
            time.sleep(TASK_DURATION_S)
            print(f"[{datetime.now().strftime('%H:%M:%M')}] Konsumer {CONSUMER_ID}: KONIEC PRACY nad zadaniem ID={task_id}.")
            
            # Zmiana statusu na 'done'
            finish_task(task_id)
            
        time.sleep(CHECK_INTERVAL_S)

if __name__ == "__main__":
    run_consumer()