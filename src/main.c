/*
 *  recv_action.cpp
 * 
 *  Program to receive action via serial port, to either
 *  heat or cool the system.
 * 
 *  Requires an appropriate script to feed actions via serial
 *  based on MQTT messages.
 * 
 *  Created by Giulio Corradini on 05/10/2020
 * 
 */

#include <msp430.h>
#include <uart.h>
#include <string.h>

#define MAX_SIZE    5

void heat() {
    P1OUT |= BIT0;
    P4OUT &= BIT7;
}

void cool() {
    P1OUT &= BIT0;
    P4OUT |= BIT7;
}

void stop() {
    P1OUT &= BIT0;
    P4OUT &= BIT7;
}

int main(void) {

    UART uart;
    uart_global_config(bps9600);
    uart_init(&uart);

    //Setup LEDs
    P1DIR |= BIT0;
    P1OUT &= BIT0;
    P4DIR |= BIT7;
    P4OUT &= BIT7;

    while(1) {
        char action[MAX_SIZE];

        int i = 0;
        do {
            uart.read(action + i, 1);
        } while(action[i++] != '\n' && i < MAX_SIZE);

        if( strncmp(action, "heat\n", 5) ) {
            heat();
        } else if ( strncmp(action, "cool\n", 5) ) {
            cool();
        } else if ( strncmp(action, "stop\n", 5) ) {
            stop();
        } else {
            uart.write("ERROR\n", 6);
        }
    }

}