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
#include <timer.h>

#define MAX_SIZE    5

int main(void) {

    UART uart;
    uart_global_config(bps9600);
    uart_init(&uart);

    //Setup LEDs
    P1DIR |= BIT0;
    P4DIR |= BIT7;

    char action;

    timer_init();
    timer_start();

    while(1) {

        uart.read(&action, 1);
        uart.write(&action, 1);

        if( action == 'h' ) {
            P1OUT |= BIT0;
            P4OUT &= ~BIT7;
        }
        if ( action == 'c' ) {
            P1OUT &= ~BIT0;
            P4OUT |= BIT7;
        }
        if ( action == 's' ) {
            P1OUT &= ~BIT0;
            P4OUT &= ~BIT7;
        }

        wait(10);

    }

}