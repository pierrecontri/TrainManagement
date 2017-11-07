#!/usr/bin/env python

import sys
import time
import difflib

import pigpio

RX=19
TX=26

MSGLEN=256

baud = int(sys.argv[1]) if len(sys.argv) > 1 else 115200
bits = int(sys.argv[2]) if len(sys.argv) > 2 else 8
runtime = int(sys.argv[3]) if len(sys.argv) > 3 else 300
ten_char_time = 100.0 / float(baud)

if ten_char_time < 0.1:
   ten_char_time = 0.1

MASK=(1<<bits)-1

# initialise test data
msg = [0] * (MSGLEN+256)
for i in range(len(msg)):
   msg[i] = i & MASK
first = 0

# Start main
pi = pigpio.pi()
#initialize the RS connection
pi.set_mode(TX, pigpio.OUTPUT)
pigpio.exceptions = False
pi.bb_serial_read_close(RX)


pi.stop()

