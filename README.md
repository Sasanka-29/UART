# UART Examples — MSP430 ↔ Python

This repository contains simple UART examples that demonstrate two-way serial communication between a PC (Python) and an MSP430 microcontroller. The examples show how to:

- Control LED blink speed on the MSP430 from the PC (send single-character commands).
- Query the MSP430 for a character from a reference array (send an index, receive a character).

Files in this repo
- BlinkLed_usingSerial.py — PC-side Python script that sends single characters ('A','B','C','D') over serial to control LED blink pace.
- BlinkLED_VariableSpeed.c — MSP430 firmware that receives single-character commands and changes LED blink speed accordingly.
- RandomValueDetection.py — PC-side Python script that requests an element of a reference array from the MSP430 by sending an index (0–9).
- SendingRandomVariables.c — MSP430 firmware that responds to index requests with the corresponding character from an internal array.

Prerequisites
- MSP430 LaunchPad (e.g., MSP430G2553 or similar with USCI_A0)
- USB-to-UART connection or LaunchPad with serial-over-USB that exposes a virtual COM port
- Python 3.x and pyserial package on host PC
  - Install pyserial: pip install pyserial
- A toolchain to build & flash MSP430 C code:
  - Code Composer Studio (CCS), or
  - msp430-gcc + mspdebug / TI flash tools (or other flashing tool you prefer)

Hardware wiring / notes
- MSP430 USCI_A0 typically maps:
  - P1.1 = RXD (UCA0RXD) — MSP430 receive pin
  - P1.2 = TXD (UCA0TXD) — MSP430 transmit pin
- On the PC side:
  - Cross TX/RX: PC Tx → MCU Rx, PC Rx → MCU Tx
  - Ground (GND) must be common between PC adapter and MSP430 board
- Baud rate used by examples: 9600 bps

Serial settings used by the code
- Baud: 9600
- Data: 8 bits
- Parity: none
- Stop bits: 1

Example 1 — Blink LED at variable speeds
- Purpose: PC sends single characters to change MSP430 blink speed.
- PC script: BlinkLed_usingSerial.py
  - Edit SERIAL_PORT variable to your platform/port (e.g., "COM3" on Windows or "/dev/ttyUSB0" on Linux/macOS).
  - Runs an infinite loop that sends 'A', 'B', 'C', 'D' repeatedly (5 seconds between sends).
  - Meaning:
    - 'A' — slow blink
    - 'B' — medium blink
    - 'C' — fast blink
    - 'D' — no blink (LED off)
- MSP430 firmware: BlinkLED_VariableSpeed.c
  - Sets MCU clock to ~1 MHz and UART to 9600 using UCA0.
  - Main loop checks the received mode (currentMode) and delays accordingly to change the blink speed on P1.0.
  - P1.0 (LED1) is toggled at different delay cycles for A/B/C; D or unknown turns the LED off.
  - Important: The code listens for single ASCII characters and changes mode.

Known issue (BlinkLED_VariableSpeed.c)
- In the RX ISR the code uses the bitwise OR operator instead of logical OR:
  - if (rxData == 'A' | rxData == 'B' | rxData == 'C' | rxData == 'D')
- This is likely unintended and should be corrected to use logical ORs (||), or better, check membership using a switch or range comparison:
  - Recommended replacement:
    - if (rxData == 'A' || rxData == 'B' || rxData == 'C' || rxData == 'D') { ... }

Example 2 — Request random/reference values by index
- Purpose: PC asks the MSP430 for a character from a small reference array by sending an index (0–9), terminated by newline. MCU responds with the character and a newline.
- PC script: RandomValueDetection.py
  - Edit the COM port in ser = serial.Serial('COM28', 9600, timeout=1) to match your system.
  - Enter index values 0–9 at the prompt. The script sends the index plus a newline and reads one line back from the MCU.
  - Compares MCU reply to the expected value in ref_list and prints Match/Mismatch.
- MSP430 firmware: SendingRandomVariables.c
  - Contains refArray[10] with characters: {'A','F','K','3','Z','Q','L','9','M','2'}.
  - Receives characters into rxBuffer until newline ('\n'), converts first received character to an index (ascii '0' → 0), validates, and sends refArray[idx] + '\n' back.
  - If index invalid, MCU sends "ERR\n".

How to build & flash the C code (general guidance)
- Using Code Composer Studio:
  - Create a new MSP430 project for your specific MCU (e.g., msp430g2553).
  - Add the .c file, build, and flash with CCS tools (Debug → Target → Program).
- Using msp430-gcc + mspdebug (example; tweak for your MCU):
  - msp430-gcc -mmcu=msp430g2553 -O2 -Wall -o SendingRandomVariables.elf SendingRandomVariables.c
  - msp430-objcopy -O ihex SendingRandomVariables.elf SendingRandomVariables.hex
  - mspdebug rf2500 "prog SendingRandomVariables.hex"   # replace rf2500 & command for your programmer
- Or use TI's UniFlash / other flashing utilities.

Running the PC scripts
1. Ensure the MSP430 is powered and flashed with the corresponding firmware.
2. Confirm the virtual COM port name and update the Python scripts:
   - BlinkLed_usingSerial.py → set SERIAL_PORT
   - RandomValueDetection.py → set serial.Serial(...) port
3. Run:
   - python BlinkLed_usingSerial.py
   - python RandomValueDetection.py

Troubleshooting
- No serial port / permission denied:
  - On Linux/macOS, make sure you have permissions (use udev rules or add your user to dialout/tty group).
  - Ensure the board is recognized and drivers installed on Windows.
- Nothing happens on MCU:
  - Check wiring (TX/RX crossed, ground common).
  - Verify correct MCU and build settings (clock calibration values present in device).
  - Make sure correct COM port and baud rate are set in Python scripts (9600).
- Unexpected characters / garbage:
  - Check baud rate, flow control settings, and ensure no other device is using the serial port.

Contributing
- Feel free to open issues or PRs to add features, fix bugs, or improve documentation.

License
- Use as-is. No license file is included; assume personal/educational use unless you add a license.

Author
- Slayer404 (repository owner)

Notes and suggestions
- Consider improving BlinkLED_VariableSpeed.c by:
  - Fixing the logical condition in the ISR (use || or switch).
  - Debouncing/clearing the UART buffer when needed.
  - Adding explicit ACKs if desired for more robust PC↔MCU protocol.
- Consider adding a small README or comments to each script with example commands and the expected output for easier onboarding.

If you want, I can:
- Add a short Makefile or example build commands for msp430-gcc,
- Patch the ISR conditional bug and create a suggested commit,
- Or create a cross-platform example that auto-detects COM ports for the PC scripts.
