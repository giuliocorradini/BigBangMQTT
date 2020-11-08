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
#include "printf.h"
#include "uart.h"
#include "timer.h"

#define MAX_SIZE    5

int main(void) {
    WDTCTL = WDTPW | WDTHOLD;

    uart_config(bps9600);


    //Setup LEDs
    P1DIR |= BIT0;
    P4DIR |= BIT7;

    while(1) {
        
        char action = uart_getchar();
        uart_putchar(action);   //echo for automatic repeat request

        if(action == 'h') {
            P1OUT |= BIT0;
            P4OUT &= ~BIT7;
        } else if (action == 'c') {
            P4OUT |= BIT7;
            P1OUT &= ~BIT0;
        } else if (action == 's') { //STOP or ON default
            P4OUT &= ~BIT7;
            P1OUT &= ~BIT0;
        } else if (action == 'o') { //OFF
            timer_start();

            P1OUT &= ~BIT0;
            P4OUT &= ~BIT7;

            int async_stat = 0;
            do {
                P1OUT ^= BIT0;
                P4OUT ^= BIT7;
                wait(1000);

                action = uart_async_getchar(&async_stat);
                if(async_stat == 0)
                    uart_putchar(action);
            } while(action != 'f');

            P1OUT &= ~BIT0;
            P4OUT &= ~BIT7;

        }

    }

}