import re

class MacFormatter:
    def __init__(self, mac_address):
        self.mac = ''.join(re.findall(r'[0-9a-f]', mac_address.lower()))
        if not re.match(r'^[0-9a-f]{12}$', self.mac):
            raise ValueError("Invalid MAC address format. Insert 12 hexadecimal characters/digits in any format.")


    def format_mac(self, delimiter, segment_length, length_mod=0, step_size=None):
        """
            Returns a formatted MAC address with specified delimiter and segment length.
            
            Args:
                delimiter (str): Delimiter between segments.
                segment_length (int): Characters in each segment.
                length_mod (int): Ensures the MAC address doesn't end with a separator. This doesn't change the actual MAC address length. Default is 0.
                step_size (int): Step size for iteration, defaults to segment_length.
        
            Returns:
                str: Formatted MAC address.
        """

        if step_size is None:
            step_size = segment_length


        try:
            return delimiter.join(
                [self.mac[i:i + segment_length] for i in range(0, len(self.mac) - length_mod, step_size)])
        except Exception as e:
            raise ValueError("Error while formatting MAC address:", e)

    @property
    def dot(self):
        return self.format_mac('.', 4, 3)

    @property
    def colon(self):
        return self.format_mac(':', 2)

    @property
    def line(self):
        return self.format_mac('-', 2)

    @property
    def space(self):
        return self.format_mac(' ', 2)

    @property
    def blank(self):
        return self.mac

