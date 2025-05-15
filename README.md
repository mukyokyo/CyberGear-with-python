## Overview

A library to process packets requested by Cybergear in a simplified manner.
It does not do much.

## Requirement

- Raspberry Pi Zero 2 W  or  Linux  or  Windows
- Pmod CAN(socketcan) or  USB-CAN I/F (gs_usb or slcan, etc.)
- Python

## Usage
1. Raspberry Pi Zero 2 W attached to DXHAT mini (tentative name).
　 Also used [Pmod CAN](https://digilent.com/reference/pmod/pmodcan/start) as CAN I/F, but anything python-can supports is ok.
   As usual, add the following to config.txt.
   ```
   dtparam=spi=on
   dtoverlay=mcp2515-can0,oscillator=20000000,interrupt=19
   dtoverlay=spi-bcm2835
   ```

   When targeting a PC, attach a USB-CAN I/F.
2. Install these tools.
   ```
   sudo apt-get install can-utils
   pip install python-can
   pip install gs_usb
   ```
5. To use socketcan with PMod CAN, perform the following operations to activate can0 beforehand.
   ```
   sudo ip link set can0 type can bitrate 1000000
   sudo ip link set can0 up
   ```

## Licence

[MIT](https://github.com/kotabrog/ft_mini_ls/blob/main/LICENSE)
