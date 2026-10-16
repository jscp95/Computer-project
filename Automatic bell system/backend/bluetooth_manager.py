import socket

class BluetoothManager:
    def __init__(self):
        self.sock = None
        self.connected = False

    def connect(self, mac_address, port=1):
        try:
            self.sock = socket.socket(
                socket.AF_BLUETOOTH,
                socket.SOCK_STREAM,
                socket.BTPROTO_RFCOMM
            )
            self.sock.connect((mac_address, port))
            self.connected = True
            return True, "Connected"
        except Exception as e:
            self.connected = False
            return False, str(e)

    def send_command(self, command="RING"):
        if not self.connected:
            return False, "Bluetooth not connected"

        try:
            self.sock.send(command.encode())
            return True, f"Sent: {command}"
        except Exception as e:
            self.connected = False
            return False, str(e)

    def disconnect(self):
        if self.sock:
            self.sock.close()
        self.connected = False
