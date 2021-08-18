import time
import os
from epics import caput, caget
from datetime import datetime
import display

d1 = display.Display("COM8")

##### COMUNICAÇÃO SERIAL DISPLAY 2 #####
# s2 = serial.Serial('COM8')
# s2.baudrate = 115200
# s2.parity = serial.PARITY_EVEN
# s2.bytesize = serial.EIGHTBITS
# s2.stopbits = serial.STOPBITS_TWO
# s2.timeout = 1
########################################


cycles = int(input("Número de clicos:"))

file_name = input("Nome o arquivo onde os dados serão salvos:")

open("{}.txt".format(file_name), "w").close()   # Clean file.

with open("{}.txt".format(file_name),'a') as f:
                f.write('Iniciado em: {}\n\n'.format(datetime.now()))
                f.write("{0:^12}{1:^12}{2:^12}{3:^12}{4:^12}{5:^12}\n\n".format("Ciclo","X","Y", "Z", "encoder_A", "encoder_B"))

# open("display_2.txt", "w").close()   # Limpa o arquivo.
# with open('display_2.txt','a') as f:
                # f.write('Iniciado em: {}\n\n'.format(datetime.now()))

os.system("cls")
print("\t\t**************\n\t\tTeste iniciado\n\t\t**************\n\n\n")
now = datetime.now()
try:
    ## Laço do Cam
    for _ in range(cycles):
        caput("IMAS2:delta-test:CamDScaling-SP", 1, wait=False)
        time.sleep(.5)
        caput("IMAS2:delta-test:EnCam-Cmd", 1, wait=False)
        
        ## Laço da leitura do apalpador
        for i in range(4):
        
            #### Lê display 1 ####
            val1, val2, val3 = d1.get()
            encoder_A = caget("IMAS2:delta-test:AxisAActualPosition-Mon", as_string=True, timeout=.5)
            encoder_B = caget("IMAS2:delta-test:AxisCActualPosition-Mon", as_string=True, timeout=.5)
            with open("{}.txt".format(file_name),'a') as f:
                f.write('{0:^12}{1:^12}{2:^12}{3:^12}{4:^12}{5:^12}\n'.format(_, val1, val2, val3, encoder_A, encoder_B,))
                print('Ciclo {5}: {0:^12}{1:^12}{2:^12}{3:^12}{4:^12}Tempo aproximado para fim do teste:\
                    {5} miinutos'.format(val1, val2, val3, encoder_A, encoder_B, _, 480-_*cycles))
        
            time.sleep(15)

except KeyboardInterrupt:
    caput("IMAS2:delta-test:EnCam-Cmd", 0, wait=False)
    print("Teste interrompido")


with open("{}.txt".format(file_name),'a') as f:
                f.write('\nDuração do teste:{}'.format(datetime.now() - now))

# with open('display_2.txt','a') as f:
                # f.write('\nDuração do teste: {}'.format(datetime.now() - now))

os.system("cls")
print("\t\t**************\n\t\tTeste finalizado\n\t\t**************\n\n\n")
print("\nDuração: {}".format(datetime.now() - now))
