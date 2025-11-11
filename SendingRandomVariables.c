#include <msp430.h>
#include <string.h>

const char refArray[10] = {'A', 'F', 'K', '3', 'Z', 'Q', 'L', '9', 'M', '2'};
char rxBuffer[5];
unsigned char rxIndex = 0;

void uartSendChar(char c) {
  while (!(IFG2 & UCA0TXIFG))
    ;
  UCA0TXBUF = c;
}
void uartSendString(const char *str) {
  while (*str) {
    uartSendChar(*str++);
  }
}
void initUART() {
  P1SEL |= BIT1 + BIT2; // Configure P1.1 & P1.2 for Tx and Rx
  P1SEL2 |= BIT1 + BIT2;

  UCA0CTL1 |= UCSWRST;
  UCA0CTL1 |= UCSSEL_2; // Set clock to SMCLK

  UCA0BR0 = 104; // 1Mhz/104= 9600
  UCA0BR1 = 0;
  UCA0MCTL = UCBRS0;

  UCA0CTL1 &= ~UCSWRST; // Reset USCI_A0
  IE2 |= UCA0RXIE;      // Enables Rx interrupt
}
int main(void) {
  WDTCTL = WDTPW | WDTHOLD;
  BCSCTL1 = CALBC1_1MHZ; // Set DCo for 1Mhz
  DCOCTL = CALDCO_1MHZ;

  initUART();
  __enable_interrupt();

  while (1)
    ;
}
#pragma vector = USCIAB0RX_VECTOR
__interrupt void USCI0RX_ISR(void) {
  char received = UCA0RXBUF; // Read the incoming byte into received

  if (received == '\n') { // If new line received it is the end of the mssg
    rxBuffer[rxIndex] = 0;
    rxIndex = 0; // reset buffer for next mssg

    int idx = rxBuffer[0] - '0'; // converts first character into integer

    if (idx >= 0 && idx < 10) {
      uartSendChar(refArray[idx]);
      uartSendChar('\n');
    } else {
      uartSendString("ERR\n");
    }
  } else {
    if (rxIndex < 4) {
      rxBuffer[rxIndex++] = received;
    }
  }
}
