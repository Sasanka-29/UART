import serial
import time

# Change this according to your system
SERIAL_PORT = "COM28"       # e.g., COM5 on Windows, "/dev/ttyUSB0" on Linux
BAUD_RATE = 9600

# Variables to send
a = 'A'
b = 'B'
c = 'C'
d = 'D'

data_list = [a, b, c, d]

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print("Serial Port Connected")

    while True:
        for value in data_list:
            message = str(value)
            ser.write(message.encode())
            if value == a:
                print(f"Sent: {value} for Slow pace blink")
            elif value == b:
                print(f"Sent: {value} for Medium blink")
            elif value == c:
                print(f"Sent: {value} for Fast blink")
            elif value == d:
                print(f"Sent: {value} for No blink")
            time.sleep(5)
except KeyboardInterrupt:
    print("Stopped by user.")

except Exception as e:
    print("Error:", e)

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial Port Closed")
