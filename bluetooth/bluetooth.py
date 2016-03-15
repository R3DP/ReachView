import time
import pexpect
import subprocess
import sys

class BluetoothError(Exception):
    """This exception is raised, when bluetoothctl fails to start."""
    pass

class Bluetooth:

    def __init__(self):
        out = subprocess.check_output("rfkill unblock bluetooth", shell = True)
        self.child = pexpect.spawn("bluetoothctl", echo = False)

    def get_output(self, command, pause = 0):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        self.child.send(command + "\n")
        time.sleep(pause)
        start_failed = self.child.expect(["bluetooth", pexpect.EOF])

        if start_failed:
            raise BluetoothError("Bluetoothctl failed after running " + command)

        return self.child.before.split("\r\n")

    def start_scan(self):
        """Start bluetooth scanning process."""
        try:
            out = self.get_output("scan on")
        except BluetoothError, e:
            print(e)
            return None

    def make_discoverable(self):
        """Make device discoverable."""
        try:
            out = self.get_output("discoverable on")
        except BluetoothError, e:
            print(e)
            return None

    def get_available_devices(self):
        """Return a list of tuples of nearby discoverable devices."""
        try:
            out = self.get_output("devices")
        except BluetoothError, e:
            print(e)
            return None
        else:
            print("Getting available devices...")
            print(out)
            available_devices = []
            print("Parsing available devices...")
            print("FULL TEXT HERE1")
            print(out)
            print("FULL TEXT HERE2")
            for line in out:
                print("Line to parse:")
                print(line)
                if "[\x1b[0;" not in line:
                    try:
                        device_position = line.index("Device")
                    except ValueError:
                        pass
                    else:
                        if device_position > -1:
                            attribute_list = line[device_position:].split(" ", 2)
                            print("Useful info:")
                            print(attribute_list)
                            mac_address = attribute_list[1]
                            name = attribute_list[2]
                            available_devices.append((mac_address, name))

            return available_devices

    def get_discoverable_devices(self):
        available = self.get_available_devices()
        paired = self.get_paired_devices()

        discoverable = []

        for dev in available:
            if dev not in paired:
                discoverable.append(dev)

        return discoverable

    def get_paired_devices(self):
        """Return a list of tuples of paired devices."""
        try:
            out = self.get_output("paired-devices")
        except BluetoothError, e:
            print(e)
            return None
        else:
            available_devices = []
            print("Parsing paired devices...")
            for line in out:
                print("Line to parse:")
                print(line)
                if "[\x1b[0;" not in line:
                    try:
                        device_position = line.index("Device")
                    except ValueError:
                        pass
                    else:
                        if device_position > -1:
                            attribute_list = line[device_position:].split(" ", 2)
                            print("Useful info:")
                            print(attribute_list)
                            mac_address = attribute_list[1]
                            name = attribute_list[2]
                            available_devices.append((mac_address, name))

            return available_devices

    def pack_device_list(self, list_of_devices):
        """Pack a list of devices to a dict."""
        devices = {}
        i = 0
        for mac_address, name in list_of_devices:
            d = {
                "name": name,
                "mac_address": mac_address
            }

            devices.update({i: d})
            i += 1

        return devices

    def get_device_info(self, mac_address):
        """Get device info by mac address."""
        try:
            out = self.get_output("info " + mac_address)
        except BluetoothError, e:
            print(e)
            return None
        else:
            return out

    def pair(self, mac_address):
        """Try to pair with a device by mac address."""
        try:
            out = self.get_output("pair " + mac_address + "\r\n", 4)
        except BluetoothError, e:
            print(e)
            return None
        else:
            return out

    def remove(self, mac_address):
        """Remove paired device by mac address, return success of the operation."""
        try:
            out = self.get_output("remove " + mac_address + "\r\n", 3)
        except BluetoothError, e:
            print(e)
            return None
        else:
            return out

    def connect(self, mac_address):
        """Try to connect to a device by mac address."""
        try:
            out = self.get_output("connect " + mac_address + "\r\n", 2)
        except BluetoothError, e:
            print(e)
            return None
        else:
            return out

    def disconnect(self, mac_address):
        """Try to disconnect to a device by mac address."""
        try:
            out = self.get_output("disconnect " + mac_address + "\r\n", 2)
        except BluetoothError, e:
            print(e)
            return None
        else:
            return out


if __name__ == "__main__":

    print("Init bluetooth...")
    bl = Bluetooth()
    print("Ready!")
    bl.get_output("scan on")
    print("Scan turned on")

    searching_for_air = True
    while searching_for_air:
        print("Scanning...")
        devices = bl.get_available_devices()
        print(devices)
        for mac, name in devices:
            if name == "air":
                searching_for_air = False
                break

    print("Found air!")
    bl.remove(mac)

    bl.get_device_info(mac)
    print("Finally pairing...")
    bl.pair(mac)

    time.sleep(3)
    print("Connecting...")
    bl.connect(mac)


















