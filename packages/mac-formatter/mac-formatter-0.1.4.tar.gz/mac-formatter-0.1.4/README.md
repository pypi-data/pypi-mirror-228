mac_format
======
A simple library for reformatting MAC-addresses.
<br />
<hr>

### How

`````pycon
from mac_formatter import MACFormation

mac_address = '01:ab:02:cd:03:ef'
mac = MACFormation(mac_address)

print(mac.dot)
print(mac.line)
print(mac.space)
print(mac.colon)
`````
output:
`````bash
01ab.02cd.03ef
01-ab-02-cd-03-ef
01 ab 02 cd 03 ef
01:ab:02:cd:03:ef
`````
<hr style="border-top: 3px solid rgba(255, 255, 255, 0.2);">
---

*thamuppet* <br>


