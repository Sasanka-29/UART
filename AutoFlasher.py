import subprocess
import sys
import serial
import time

ref_list = ['A', 'F', 'K', '3', 'Z', 'Q', 'L', '9', 'M', '2']

ser = serial.Serial('COM28', 9600)
time.sleep(2)

HEX_FILE = r"C:\Users\sasan\workspace_ccstheia\Sending_RandomValue_UART\Debug\Sending_RandomValue_UART.hex"
PORT = "COM24"
MSP_TOOL = r"C:\ti\MSPFlasher_1.3.20\MSP430Flasher.exe"



def request_char(index):  #sends index to MSP and returns a reply
    ser.write(f"{index}\n".encode())  #converts index into a string and sends it to MSP
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    return response


def flash_msp430():
    print("\n Flashing Code into MSP-EXP430G2ET...")

    cmd = [MSP_TOOL,"-w", HEX_FILE, "-v", "-g", "-z", "[VCC]", "-i", PORT]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)

        print("\n--- MSPFlasher Output ---")
        print(result.stdout)

        if "Error" in result.stdout or result.returncode != 0:
            print("Flashing Failed!")
        else:
            print("Flash Successful!")

    except Exception as e:
        print("Flashing process crashed:", e)


# Command loop
while True:
    user = input("\nEnter 'f' to flash, 'q' to quit: ").strip().lower()

    if user == 'f':
        flash_msp430()
    elif user == 'q':
        sys.exit("Exiting")
    else:
        print("Invalid option")

    idx = input("\nEnter index (0-9) to request or x to exit: ")

    if idx.lower() != 'x':
        if idx.isdigit() and (0 <= int(idx) <= 9):  #Prevent non-integer inputs and then converts string to int
            received = request_char(idx)  #Calls request_char function to send an index to MSP and get a reply
            expected = ref_list[int(idx)]  #looks up the expected value in ref_list

            print("MSP430 replied :", received)
            print("Expected       :", expected)

            if received == expected:
                print("Match!\n")
            else:
                print("Mismatch\n")
            continue

        print("Invalid input, enter 0-9")

    break
ser.close()