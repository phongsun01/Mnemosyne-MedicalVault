import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logger = logging.getLogger(__name__)

class NewFileHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback

    def on_created(self, event):
        if not event.is_directory:
            logger.info(f"New file detected: {event.src_path}")
            # Wait a bit for file to be fully written
            time.sleep(1)
            self.callback(event.src_path)

def start_watcher(path, callback):
    event_handler = NewFileHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    logger.info(f"Watcher started on: {path}")
    return observer
