import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from common import SerialPortWatcher

# Handles events from the FS watchdog
class ChangeHandler(FileSystemEventHandler):

    # A file has been created
    def on_created(self, event):
        # Ignore noise from directories
        if not event.is_directory:
            # Tell watcher a change might have been made
            watcher.notify()

    # A file has been deleted
    def on_deleted(self, event):
        # Ignore noise from directories
        if not event.is_directory:
            # Tell watcher a change might have been made
            watcher.notify()

# Linux entry point
def linux_main():
    # Initialize common logic
    global watcher
    watcher = SerialPortWatcher()

    # Initialize change handler
    path = "/dev"
    event_handler = ChangeHandler()

    # Initialize and start observer
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()
    print(f"Observer active on {path}")

    # Idle loop
    try:
        # Loop while exit isn't requested
        while not watcher.exitRequested:
            time.sleep(1)

        # Loop exited normally (user clicked Exit), stop the observer
        observer.stop()
    except KeyboardInterrupt:
        # Ctrl-C was pressed, stop the observer
        observer.stop()

    # Wait for observer to exit
    observer.join()
    print("Observer deactivated")

    # Clean up common logic
    watcher.cleanup()