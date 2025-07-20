import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from anomaly_detector import detect_anomalies

print("✅ Anomaly detector initialized.")

class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".log"):
            with open(event.src_path, 'r') as f:
                lines = f.readlines()
                if lines:
                    detect_anomalies(lines[-10:])  # Analyze last 10 lines

if __name__ == "__main__":
    path = "../logs"  # Still one level up from backend
    if not os.path.exists(path):
        print("❌ Log folder not found:", path)
        exit(1)

    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    print("📡 Monitoring logs in:", path)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
