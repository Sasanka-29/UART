#include <msp430.h>
#include <stdbool.h>

#define LED1 BIT0 // P1.0 Green
#define LED2 BIT6 // P1.6 Red
volatile char rxData = 0;
volatile char currentMode = 0;

void initClock1MHz(void) {
  if (CALBC1_1MHZ == 0xFF)
    while (1)
      ;
  BCSCTL1 = CALBC1_1MHZ;
  DCOCTL = CALDCO_1MHZ;
}

void initUART9600(void) {
  P1SEL |= BIT1 + BIT2;
  P1SEL2 |= BIT1 + BIT2;

  UCA0CTL1 |= UCSWRST;
  UCA0CTL1 |= UCSSEL_2;

  UCA0BR0 = 104;
  UCA0BR1 = 0;
  UCA0MCTL = UCBRS0;

  UCA0CTL1 &= ~UCSWRST;
  IE2 |= UCA0RXIE;
}

int main(void) {
  WDTCTL = WDTPW + WDTHOLD;
  initClock1MHz();
  P1DIR |= LED1 | LED2;    // Set P1.0 and P1.6 as output
  P1OUT &= ~(LED1 | LED2); // Turn both OFF initially

  initUART9600();

  __enable_interrupt();
  __bis_SR_register(LPM0_bits + GIE); // Sleep until UART interrupt

  while (1) {
    if (currentMode == 'A') {
      P1OUT ^= LED1;
      // P1OUT &= ~LED2;
      __delay_cycles(150000);

    } else if (currentMode == 'B') {
      P1OUT ^= LED1;
      // P1OUT &= ~LED1;
      __delay_cycles(100000);

    } else if (currentMode == 'C') {
      P1OUT ^= LED1;
      // P1OUT &= ~LED1;
      __delay_cycles(50000);
    } else {
      P1OUT &= ~LED1;
      // P1OUT &= ~LED2;
    }
  }
}

#pragma vector = USCIAB0RX_VECTOR
__interrupt void USCI0RX_ISR(void) {
  rxData = UCA0RXBUF;

  if (rxData == 'A' | rxData == 'B' | rxData == 'C' | rxData == 'D') {
    currentMode = rxData;
  } else {
    currentMode = 0;
  }
  __bic_SR_register_on_exit(LPM0_bits); // Wake up MCU
}

