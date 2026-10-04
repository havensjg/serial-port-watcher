import serial.tools.list_ports

# Common logic for all platforms
class SerialPortWatcher:

    # Constructor 
    def __init__(self):
        # Initialize fields
        self.closeRequested = False
        self.lastPorts = serial.tools.list_ports.comports()

        # For debug purposes, print the serial ports already attached
        portList = [port.device for port in self.lastPorts]
        print(f"Ports already attached: {portList}")

    # Clean up any resources before closing
    def cleanup(self):
        pass

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
        print(f"{port.device} attach")
        print(f"    Name: {port.name}")
        print(f"    Description: {port.description}")
        print(f"    Hardware ID: {port.hwid}")

    # Notify that a device was detached
    def notifyDetach(self, port):
        print(f"{port.device} detach")
        print(f"    Name: {port.name}")
        print(f"    Description: {port.description}")
        print(f"    Hardware ID: {port.hwid}")