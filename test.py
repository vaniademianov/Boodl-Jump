import serial
ser = serial.Serial("COM8")
while True:
    v = ser.read_all()
    if len(v) != 0:
        print(v)
