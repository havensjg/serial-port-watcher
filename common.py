from PIL import Image
import pystray
import serial.tools.list_ports
import threading
import webbrowser

# Common logic for all platforms
class SerialPortWatcher:

    # Constructor 
    def __init__(self):
        # Initialize fields
        self.exitRequested = False
        self.lastPorts = serial.tools.list_ports.comports()

        # For debug purposes, print the serial ports already attached
        portList = [port.device for port in self.lastPorts]
        print(f"Ports already attached: {portList}")

        # Initialize tray icon and menu
        self.initMenu()

    # Clean up any resources before closing
    def cleanup(self):
        # Clean up the tray icon
        if self.icon:
            self.icon.stop()

        # Join the tray icon thread
        if self.iconThread:
            self.iconThread.join()

    # Initialize tray icon and menu
    def initMenu(self):
        # Load icon, if that fails, just make it a red square
        try:
            # Try to load icon
            image = Image.open("icon.png")
            image.load()
        except Exception as e:
            # Loading icon failed for whatever reason, make a placeholder instead
            print(e)
            image = Image.new("RGB", (64, 64), color="red")

        # Set up menu
        about_menu = pystray.Menu(
            pystray.MenuItem("Serial Port Watcher", lambda icon, item: None, enabled=False),
            pystray.MenuItem("(c) 2026 Joseph Havens", lambda icon, item: None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Visit GitHub repository", lambda icon, item: webbrowser.open("https://github.com/havensjg/serial-port-watcher"))
        )
        menu = pystray.Menu(
            pystray.MenuItem("About", about_menu),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", lambda icon, item: self.menuExit())
        )

        # Set up icon
        self.icon = pystray.Icon(
            name="Serial Port Watcher",
            icon=image,
            title="Serial Port Watcher",
            menu=menu
        )

        # Create thread for icon loop
        self.iconThread = threading.Thread(
            target=lambda icon: icon.run(),
            args=[self.icon]
        )
        self.iconThread.start()

    # Called when the "Exit" item is used on the tray menu
    def menuExit(self):
        print("Exit requested")
        self.exitRequested = True

    # Called when a device tree change has been made. Re-enumerates the serial ports and notifies on any changes
    def notify(self):
        newPorts = serial.tools.list_ports.comports()

        # Check for detach
        for p in self.lastPorts:
            # Is this port in the new list?
            found = False
            for n in newPorts:
                if n.device == p.device:
                    found = True

            # If it wasn't found in the new list, it must have detached
            if not found:
                self.notifyDetach(p)
        
        # Check for attach
        for n in newPorts:
            # Is this port in the old list?
            found = False
            for p in self.lastPorts:
                if n.device == p.device:
                    found = True

            # If it wasn't found in the old list, it must have attached
            if not found:
                self.notifyAttach(n)

        # Update the lastPorts list
        self.lastPorts = newPorts

    # Notify that a device was attached
    def notifyAttach(self, port):
        # Log details
        print(f"{port.device} attach")
        print(f"    Name: {port.name}")
        print(f"    Description: {port.description}")
        print(f"    Hardware ID: {port.hwid}")

        # Popup
        self.popup(f"{port.name} attached", port.description)

    # Notify that a device was detached
    def notifyDetach(self, port):
        # Log details
        print(f"{port.device} detach")
        print(f"    Name: {port.name}")
        print(f"    Description: {port.description}")
        print(f"    Hardware ID: {port.hwid}")

        # Popup
        self.popup(f"{port.name} detached", port.description)

    # Popup message
    def popup(self, title, message):
        self.icon.notify(message, title=title)