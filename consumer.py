import csv
import os
import time
import uuid
from datetime import datetime

QUEUE_FILE = 'tasks.csv'
STATUS_PENDING = 'pending'
STATUS_IN_PROGRESS = 'in_progress'
STATUS_DONE = 'done'
TASK_DURATION_S = 30
CHECK_INTERVAL_S = 5

# Unikalny identyfikator tego konsumera
CONSUMER_ID = str(uuid.uuid4())[:8]

def process_task():
    """
    1. Odczytuje wszystkie zadania.
    2. Znajduje pierwsze zadanie 'pending'.
    3. Zmienia jego status na 'in_progress' i zapisuje consumer_id.
    4. Zapisuje zmienioną listę do pliku.
    5. Wykonuje pracę (30s sleep).
    6. Zmienia status na 'done' i ponownie zapisuje do pliku.
    """
    
    # 1. Odczyt wszystkich zadań
    tasks = []
    task_to_process = None
    task_index = -1
    
    if not os.path.exists(QUEUE_FILE):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Konsumer {CONSUMER_ID}: Plik kolejki nie istnieje.")
        return

    try:
        with open(QUEUE_FILE, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader) # Zapisanie nagłówka
            
            for i, row in enumerate(reader):
                tasks.append(row)
                
                # 2. Znalezienie pierwszego zadania 'pending'
                # Kolumny: 0=id, 1=status, 2=creation_time, 3=consumer_id
                if task_to_process is None and len(row) > 1 and row[1] == STATUS_PENDING:
                    task_to_process = row
                    task_index = i
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Konsumer {CONSUMER_ID}: Błąd odczytu pliku: {e}")
        return

    if task_to_process:
        task_id = task_to_process[0]
        
        # 3. Zmiana statusu na 'in_progress'
        # Aktualizacja w liście 'tasks'
        tasks[task_index][1] = STATUS_IN_PROGRESS
        tasks[task_index][3] = CONSUMER_ID 
        
        # 4. Zapis zmienionej listy do pliku (zabezpieczenie: tryb 'w' nadpisuje)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Konsumer {CONSUMER_ID}: POBRANO zadanie ID={task_id}. Status -> {STATUS_IN_PROGRESS}")
        
        try:
            with open(QUEUE_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header) # Zapis nagłówka
                writer.writerows(tasks) # Zapis zadań
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Konsumer {CONSUMER_ID}: Błąd zapisu IN_PROGRESS: {e}")
            return
            
        # 5. Wykonanie pracy (30s sleep)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Konsumer {CONSUMER_ID}: START PRACY nad zadaniem ID={task_id}. Czas: {TASK_DURATION_S}s.")
        time.sleep(TASK_DURATION_S)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Konsumer {CONSUMER_ID}: KONIEC PRACY nad zadaniem ID={task_id}.")

        # 6. Zmiana statusu na 'done' i ponowny zapis
        tasks[task_index][1] = STATUS_DONE
        
        try:
            with open(QUEUE_FILE, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(tasks)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Konsumer {CONSUMER_ID}: ZAKOŃCZONO zadanie ID={task_id}. Status -> {STATUS_DONE}")
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Konsumer {CONSUMER_ID}: Błąd zapisu DONE: {e}")


def run_consumer():
    print(f"Konsumer {CONSUMER_ID} uruchomiony. Sprawdzanie co {CHECK_INTERVAL_S}s.")
    while True:
        process_task()
        time.sleep(CHECK_INTERVAL_S)

if __name__ == "__main__":
    run_consumer()