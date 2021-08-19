import logging
import time
import typing

import serial

logger = logging.getLogger(__file__)
formatter = logging.Formatter(
    "[%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(funcName)s] %(message)s"
)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class Display:
    """This class represents the couple display + touch probe."""

    def __init__(self, port: str):
        self._sport: typing.Optional[serial.Serial] = None
        self._encoding = "utf-8"
        try:
            self._sport = serial.Serial(port)
            self._sport.baudrate = 115200
            self._sport.parity = serial.PARITY_EVEN
            self._sport.bytesize = serial.EIGHTBITS
            self._sport.stopbits = serial.STOPBITS_TWO
            self._sport.timeout = 1
        except Exception:
            #   logger.debug()
            #   logger.info()
            #   logger.warning()
            #   logger.error()
            logger.exception("sport1 has not been started")

    def get(self):
        if not self._sport:
            raise RuntimeError("Serial port is closed")

        self._sport.write(b"\x1bA0200\r")
        time.sleep(0.2)
        readings = self._sport.read_all().decode(self._encoding)
        readings = readings.upper().split(" R\r\n")
        val1 = readings[0][readings[0].find("X=") + 2 :]
        val1 = val1.replace(" ", "")
        val2 = readings[1][readings[1].find("Y=") + 2 :]
        val2 = val2.replace(" ", "")
        val3 = readings[2][readings[2].find("Z=") + 2 :]
        val3 = val3.replace(" ", "")
        return [val1, val2, val3]
