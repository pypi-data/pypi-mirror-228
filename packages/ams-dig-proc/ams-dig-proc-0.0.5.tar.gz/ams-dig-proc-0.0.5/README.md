# AMS-DIG-PROC python library

<img src="docs/source/ams-dig-proc_small.jpg" style="float: right;">

[AMS-DIG-PROC board](https://vigophotonics.com/products/infrared-detection-modules/accessories/accessories-to-the-ams-detection-module-series/) is an digital extension board to AMS family od infrared detection modules.

This repository contains python libraries and C source files to handle communication with the board.

## Python installation
```bash
pip install ams-dig-proc
```

## C usage
There is a header file available (`C/Inc/protocol.h`)
It contains definitions of all messages required to work with AMS-DIG-PROC board.

`C/Src/ams_dig_proc_crc.c` contains function that can be used for CRC calculations.

There is no special requirements or installation procedure for C.

## Examples and documentation
There are many examples available in the [documentation](https://ams-dig-proc.readthedocs.io/en/latest/index.html)

