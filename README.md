## Overview

Connect PmodCAN to raspberry pi zero 2 W and communicate with CyberGear.
The treatment of endianness was done according to the results and may be flawed.

## Requirement

- Raspberry Pi Zero 2 W
- Pmod CAN
- Python

## Usage
1. Raspberry Pi Zero 2 W attached to DXHAT mini (tentative name).
2. Also used [Pmod CAN](https://digilent.com/reference/pmod/pmodcan/start) as CAN I/F, but anything python-can supports is ok.
3. As usual, add the following to config.txt.
   ```
   dtparam=spi=on
   dtoverlay=mcp2515-can0,oscillator=20000000,interrupt=19
   dtoverlay=spi-bcm2835
   ```
4. Install these tools.
   ```
   sudo apt-get install can-utils
   pip install python-can --break-system-packages
   ```
5. Activate can0.
   ```
   sudo ip link set can0 type can bitrate 1000000
   sudo ip link set can0 up
   ```

## Licence

[MIT](https://github.com/kotabrog/ft_mini_ls/blob/main/LICENSE)
