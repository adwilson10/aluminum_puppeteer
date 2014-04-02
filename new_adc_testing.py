#!/usr/bin/python

import serial
import matplotlib.pyplot as mp
import time
import sys


def open_comm(device='/dev/ttyUSB0',
              baud=115200,
              stop=2):
    """
    Function for opening comport
    """
    global OS
    print "opening serial port:", device
    try:
        s = serial.Serial(device)
        s.close()
        comport = serial.Serial(device,
                                baudrate=baud,
                                timeout=0.5,
                                parity=serial.PARITY_NONE,
                                stopbits=stop,
                                rtscts=False)
    except (serial.SerialException, ValueError):
        print "Could not open serial port", device+"!"
        sys.exit(1)

    comport.flushInput()
    comport.flushOutput()
    return comport


def close_comm(comport):
    print "closing comm port"
    comport.close()


def unlock_pic(com):
    # time.sleep(0.5)
    cmd = 'm1\x00\x00\x00\x00\x00\x00\x00\x00\x00a'
    com.write(cmd)

def request_data(com):
    # send command to request data PIC
    com.flushInput()
    com.flushOutput()
    cmd = 'z1' + chr(0x54)
    com.write(cmd)
    dat = []
    # read in all data:
    err_flag = False
    while not err_flag:
        ln = com.read(size=10)
        if len(ln) < 10:
            err_flag = True
        ln = ln.splitlines()
        try:
            ln = ln[0]
            dat.append(int(ln.strip('\x00')))
        except:
            pass
    mp.plot(dat)
    mp.show()
    mp.close()
    mp.cla()
    mp.clf()
    return dat

def dat_print(data):
    errs = []
    for i,d in enumerate(data):
        print "index = ",i,"data[i] = ",d
        if abs(i-d) > 1e-3:
            errs.append(i)
    print "Errors: num errors = ", len(errs),"num dat = ",len(data)
    print errs
    return


com = open_comm()

data = []
while True:
    question = "q = quit, m = unlock, z = request, d = print dat\r\n"
    ans = raw_input(question)
    if ans is 'q':
        break
    elif ans is 'z':
        data = request_data(com)
    elif ans is 'm':
        unlock_pic(com)
    elif ans is  'd':
        dat_print(data)
    else:
        print "Unrecognized command!"

close_comm(com)

