import subprocess
import sys

HEX_FILE = r"C:\ti\MSPFlasher_1.3.20\BlinkRedLED_MSP-EXP430G2ET.hex"
PORT = "COM24"
MSP_TOOL = r"C:\ti\MSPFlasher_1.3.20\MSP430Flasher.exe"


def flash_msp430():
    print("\n Flashing MSP430...")

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
