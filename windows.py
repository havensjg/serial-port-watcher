import time
import win32api
import win32con
import win32gui

from common import SerialPortWatcher

# Device notification constants
WM_DEVICECHANGE = 0x0219

DBT_DEVICEARRIVAL = 0x8000
DBT_DEVICEREMOVECOMPLETE = 0x8004

# Window message handler
def window_proc(hwnd, msg, wparam, lparam):
    # Check device change messages
    if msg == WM_DEVICECHANGE:
        # Did a device connect?
        if wparam == DBT_DEVICEARRIVAL:
            # Tell watcher a change might have been made
            watcher.notify()
        
        # Did a device disconnect?
        elif wparam == DBT_DEVICEREMOVECOMPLETE:
            # Tell watcher a change might have been made
            watcher.notify()

        return 0

    # Window destruction requested
    if msg == win32con.WM_DESTROY:
        win32gui.PostQuitMessage(0)
        return 0

    # Message not handled, use default handler
    return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)

# Windows entry point
def windows_main():
    # Initialize common logic
    global watcher
    watcher = SerialPortWatcher()

    # Create a window class
    wc = win32gui.WNDCLASS()
    wc.lpfnWndProc = window_proc
    wc.lpszClassName = "SerialPortWatcher"
    wc.hInstance = win32api.GetModuleHandle(None)
    class_atom = win32gui.RegisterClass(wc)

    # Create an invisible window
    hwnd = win32gui.CreateWindow(
        class_atom,              # Window class
        "Serial Port Watcher",   # Window title 
        0,                       # No visible window style
        0, 0, 0, 0,              # Window position and size
        0,                       # Parent HWND
        0,                       # Menu handle
        wc.hInstance,            # Instance handle
        None                     # Parameter
    )

    # Process Windows messages
    print("Message loop active")
    while not watcher.exitRequested:
        # Process windows messages
        win32gui.PumpWaitingMessages()

        # Prevent 100% CPU usage
        time.sleep(0.1)

    # Exit requested, destroy window
    win32gui.DestroyWindow(hwnd)

    # Let the messages process. PumpMessages will exit when it gets the quit message
    win32gui.PumpMessages()
    print("Message loop deactivated")

    # Clean up common logic
    watcher.cleanup()