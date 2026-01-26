import csv
import os
import time
from datetime import datetime

QUEUE_FILE = 'tasks.csv'
STATUS_PENDING = 'pending'

def get_next_id():
    """Zwraca unikalny ID dla nowego zadania, czytając ostatni ID z pliku."""
    if not os.path.exists(QUEUE_FILE):
        return 1
    
    with open(QUEUE_FILE, mode='r', newline='') as file:
        reader = csv.reader(file)
        # Omijanie nagłówka
        try:
            next(reader) 
        except StopIteration:
            return 1 # Pusty plik

        last_id = 0
        for row in reader:
            try:
                # Oczekujemy ID w pierwszej kolumnie
                last_id = max(last_id, int(row[0])) 
            except (ValueError, IndexError):
                # Ignoruj źle sformatowane wiersze
                continue
        return last_id + 1


def add_task_to_queue():
    """Dodaje nowe zadanie do pliku-kolejki."""
    task_id = get_next_id()
    
    # Dane nowego zadania
    new_task = [
        task_id,
        STATUS_PENDING,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        '' # Miejsce na consumer_id
    ]

    # Nagłówek - tylko jeśli plik nie istnieje lub jest pusty
    file_exists = os.path.exists(QUEUE_FILE)
    write_header = not file_exists or os.path.getsize(QUEUE_FILE) == 0

    with open(QUEUE_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        if write_header:
            writer.writerow(['id', 'status', 'creation_time', 'consumer_id'])
            
        writer.writerow(new_task)
        
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ZADANIE DODANE: ID={task_id}, Status={STATUS_PENDING}")

if __name__ == "__main__":
    add_task_to_queue()