import serial

class Display:
    """This class represents the couple display + touch probe."""

    def __init__(port1, port2):
        try:
            sport = serial.Serial(str(port))
            sport.baudrate = 115200
            sport.parity = serial.PARITY_EVEN
            sport.bytesize = serial.EIGHTBITS
            sport.stopbits = serial.STOPBITS_TWO
            sport.timeout = 1
        except:
            print("sport1 has not been started")

        def get(self):
            port = self.sport
            port.write(b'\x1bA0200\r')
            time.sleep(0.2)
            reading = port.read_all().decode('utf-8')
            readings = readings.upper().split(' R\r\n')
            val1 = readings[0][readings[0].find('X=') + 2:]
            val1 = val1.replace(' ', '')
            val2 = readings[1][readings[1].find('Y=') + 2:]
            val2 = val2.replace(' ', '')
            val3 = readings[2][readings[2].find('Z=') + 2:]
            val3 = val3.replace(' ', '')
            return([val1, val2, val3])
