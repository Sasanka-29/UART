import serial
import time

# Same reference table
ref_list = ['A','F','K','3','Z','Q','L','9','M','2']

# Configure port (change COM port as per your system)
ser = serial.Serial('COM28', 9600, timeout=1)
time.sleep(2)

def request_char(index):
    ser.write(f"{index}\n".encode())
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    return response

while True:
    idx = input("Enter index (0-9) to request or x to exit: ")

    if idx.lower() == 'x':
        break

    if not idx.isdigit() or not (0 <= int(idx) <= 9):
        print("Invalid input, enter 0-9")
        continue

    received = request_char(idx)
    expected = ref_list[int(idx)]

    print("MSP430 replied :", received)
    print("Expected       :", expected)

    if received == expected:
        print("Match!\n")
    else:
        print("Mismatch\n")

ser.close()
