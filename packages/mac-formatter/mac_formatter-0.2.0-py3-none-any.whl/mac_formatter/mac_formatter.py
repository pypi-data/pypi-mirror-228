import re

class MacFormatter:
    def __init__(self, mac_address):
        try:
            self.mac = re.sub(r'[:\-\\.%@"\'+/= ]', '', mac_address.lower())
            if not re.match(r'^[0-9a-f]{12}$', self.mac):
                raise ValueError("Invalid MAC address format. Insert 12 hexadecimal characters/digits in any format.")
        except Exception as e:
            raise ValueError("Error while processing MAC address:", e)

    def format_mac(self, char, space, x, y):
        try:
            return f'{char}'.join([self.mac[i:i + space] for i in range(0, len(self.mac) - x, y)])
        except Exception as e:
            raise ValueError("Error while formatting MAC address:", e)

    @property
    def dot(self):
        return self.format_mac('.', 4, 3, 4)

    @property
    def colon(self):
        return self.format_mac(':', 2, 0, 2)

    @property
    def line(self):
        return self.format_mac('-', 2, 0, 2)

    @property
    def space(self):
        return self.format_mac(' ', 2, 0, 2)
