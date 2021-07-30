import socket
import enum


class Effect(enum.Enum):
    CONFETTI = 0
    FIRE = 1
    RAINBOW_VERTICAL = 2
    RAINBOW_HORIZONTAL = 3
    COLOR = 4
    CRAZY = 5
    CLOUDS = 6
    LAVA = 7
    PLASMA = 8
    RAINBOW = 9
    PAVLIN = 10
    ZEBRA = 11
    FOREST = 12
    OCEAN = 13
    COLOR2 = 14
    SNOW = 15
    MATRIX = 16
    LIGHTERS = 17


class Lamp:
    def __init__(self, address: str, port=8888):
        self.address = (address, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.is_enabled = False
        self._effect = 0
        self._brightness = 0
        self._speed = 0
        self._scale = 0
        if not self.update_status():
            raise socket.timeout

    def update_status(self):
        # ['CURR', '1', '227', '19', '1', '0']
        self.sock.sendto(b"GET", self.address)
        return self._parse_input_()

    def _parse_input_(self):
        self.sock.settimeout(1)
        while True:
            try:
                input_data = self.sock.recv(1024).decode().split(" ")
                print("DEBUG INPUT:", input_data)
            except socket.timeout:
                return None
            if not isinstance(input_data, list):
                raise ValueError("Receive bad response", input_data)
            if input_data[0] == "CURR":
                self.is_enabled = input_data[5] == "1"
                self._effect = Effect(int(input_data[1]))
                self._brightness = int(input_data[2])
                self._speed = int(input_data[3])
                self._scale = int(input_data[4])
            if input_data[0] == "BRI":
                self._brightness = int(input_data[1])
            if input_data[0] == "SPD":
                self._speed = int(input_data[1])
            return input_data

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, value: (int, Effect)):
        if isinstance(value, int):
            self.sock.sendto(f"EFF {value}".encode("ascii"), self.address)
        if isinstance(value, Effect):
            self.sock.sendto(f"EFF {value.value}".encode("ascii"), self.address)
        self._parse_input_()

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, brightness: int):
        self.sock.sendto(f"BRI {brightness}".encode("ascii"), self.address)
        self._parse_input_()

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed: int):
        self.sock.sendto(f"SPD {speed}".encode("ascii"), self.address)
        self._parse_input_()

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale: int):
        self.sock.sendto(f"SCA {scale}".encode("ascii"), self.address)
        self._parse_input_()

    def enable(self):
        self.sock.sendto(b"P_ON", self.address)
        self._parse_input_()

    def disable(self):
        self.sock.sendto(b"P_OFF", self.address)
        self._parse_input_()

    def __str__(self):
        return f"LAMP{self.address} - Enabled: {'YES' if self.is_enabled else 'NO'}, " \
               f"Effect: {self.effect}, Brightness: {self.brightness}, Speed: {self.speed}, Scale: {self.scale}"
