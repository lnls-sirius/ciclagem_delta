import os
import time
from datetime import datetime

import serial
from epics import caget, caput

##### COMUNICAÇÃO SERIAL DISPLAY 1 #####
s = serial.Serial("COM8")
s.baudrate = 115200
s.parity = serial.PARITY_EVEN
s.bytesize = serial.EIGHTBITS
s.stopbits = serial.STOPBITS_TWO
s.timeout = 1
########################################

##### COMUNICAÇÃO SERIAL DISPLAY 2 #####
# s2 = serial.Serial('COM8')
# s2.baudrate = 115200
# s2.parity = serial.PARITY_EVEN
# s2.bytesize = serial.EIGHTBITS
# s2.stopbits = serial.STOPBITS_TWO
# s2.timeout = 1
########################################

# caput("IMAS2:delta-test:EnCam-Cmd", 0, wait=False)


# def handle_pv_change(pvname=None, value=None, char_value=None, **kwds):
#   if value != "":
#       return

# camonitor("IMAS2:delta-test:EnCam-Cmd", callback=handle_pv_change)

ciclos = int(input("Número ciclos:"))

file_name = input("Nome o arquivo onde os dados serão salvos:")
open("{}.txt".format(file_name), "w").close()  # Limpa o arquivo.

with open("{}.txt".format(file_name), "a") as f:
    f.write("Iniciado em: {}\n\n".format(datetime.now()))
    f.write(
        "{0:^12}{1:^12}{2:^12}{3:^12}{4:^12}\n\n".format(
            "X", "Y", "Z", "ENCODER_A", "ENCODER_C"
        )
    )

# open("display_2.txt", "w").close()   # Limpa o arquivo.
# with open('display_2.txt','a') as f:
# f.write('Iniciado em: {}\n\n'.format(datetime.now()))

os.system("cls")
print("\t\t**************\n\t\tTeste iniciado\n\t\t**************\n\n\n")
now = datetime.now()
try:
    ## Laço do Cam
    for _ in range(ciclos):
        caput("IMAS2:delta-test:CamDScaling-SP", 1, wait=False)
        time.sleep(0.5)
        caput("IMAS2:delta-test:EnCam-Cmd", 1, wait=False)

        ## Laço da leitura do apalpador
        for i in range(4):
            if i == 0:
                time.sleep(14)
            if i == 1:
                time.sleep(28)
            if i == 3:
                time.sleep(14.5)
            if i != 2:
                #### Lê display 1 ####
                s.write(b"\x1bA0200\r")
                time.sleep(0.2)
                readings = s.read_all().decode("utf-8")
                readings = readings.upper().split(" R\r\n")
                val1 = readings[0][readings[0].find("X=") + 2 :]
                val1 = val1.replace(" ", "")
                val2 = readings[1][readings[1].find("Y=") + 2 :]
                val2 = val2.replace(" ", "")
                val3 = readings[2][readings[2].find("Z=") + 2 :]
                val3 = val3.replace(" ", "")
                encoder_A = caget(
                    "IMAS2:delta-test:AxisAActualPosition-Mon",
                    as_string=True,
                    timeout=0.5,
                )
                encoder_C = caget(
                    "IMAS2:delta-test:AxisCActualPosition-Mon",
                    as_string=True,
                    timeout=0.5,
                )
                with open("{}.txt".format(file_name), "a") as f:
                    f.write(
                        "{}\t{}\t{}\t{}\t{}\n".format(
                            val1, val2, val3, encoder_A, encoder_C
                        )
                    )
                    print(
                        "{0:^12}{1:^12}{2:^12}{3:^12}{4:^12}".format(
                            val1, val2, val3, encoder_A, encoder_C
                        )
                    )


except KeyboardInterrupt:
    caput("IMAS2:delta-test:EnCam-Cmd", 0, wait=False)
    print("Fim do Cam")


with open("{}.txt".format(file_name), "a") as f:
    f.write("\nDuração do teste:{}".format(datetime.now() - now))

# with open('display_2.txt','a') as f:
# f.write('\nDuração do teste: {}'.format(datetime.now() - now))

os.system("cls")
print("\t\t**************\n\t\tTeste finalizado\n\t\t**************\n\n\n")
print("\nDuração: {}".format(datetime.now() - now))
