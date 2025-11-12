import serial
import time

ref_list = ['A', 'F', 'K', '3', 'Z', 'Q', 'L', '9', 'M', '2']

ser = serial.Serial('COM28', 9600)
time.sleep(2)


def request_char(index):  #sends index to MSP and returns a reply
    ser.write(f"{index}\n".encode())  #converts index into a string and sends it to MSP
    time.sleep(0.1)
    response = ser.readline().decode().strip()
    return response


while True:
    idx = input("Enter index (0-9) to request or x to exit: ")

    if idx.lower() == 'x':
        break

    if not idx.isdigit() or not (0 <= int(idx) <= 9):  #Prevent non-integer inputs and then converts string to int
        print("Invalid input, enter 0-9")
        continue

    received = request_char(idx)  #Calls request_char function to send an index to MSP and get a reply
    expected = ref_list[int(idx)]  #looks up the expected value in ref_list

    print("MSP430 replied :", received)
    print("Expected       :", expected)

    if received == expected:
        print("Match!\n")
    else:
        print("Mismatch\n")

ser.close()
