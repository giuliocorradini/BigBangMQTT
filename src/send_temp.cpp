/*
 *  adConvSerialTempTx
 *  by Giulio Corradini
 * 
 *  from bigBangMQTT assignment
 * 
 *  depends on libmsp430 (https://github.com/giuliocorradini/libmsp430)
 *  to fetch it run
 *      git submodule init
 *      git submodule update
 * 
 *  Thermometer MSP430
 * 
 */

#include <msp430.h>
#include "uart.h"
#include "adc.h"
#include "string.h"
#include "printf.h"
#include "timer.h"

using namespace sensor;

#define CALADC12_15V_30C  *((unsigned int *)0x1A1A)
#define CALADC12_15V_85C  *((unsigned int *)0x1A1C)

volatile bool on = false;

int main_pub(void) {
    WDTCTL = WDTPW | WDTHOLD;

    P1DIR |= BIT0;

    //Switch 1: set t_max
    P2DIR &= ~BIT1;
    P2REN |= BIT1;
    P2OUT |= BIT1;
    P2IES |= BIT1;
    P2IE |= BIT1;

    //Switch 2: set t_min
    P1DIR &= ~BIT1;
    P1REN |= BIT1;
    P1OUT |= BIT1;
    P1IES |= BIT1;
    P1IE |= BIT1;

    //On/Off switch
    P1DIR &= ~BIT2;
    P1REN |= BIT2;
    P1OUT |= BIT2;

    timer_start();
    __enable_interrupt();

    int bits30 = CALADC12_15V_30C;
    int bits85 = CALADC12_15V_85C;
    float degC_per_bit = 55.0f/(float)(bits85-bits30);   //conversion slope

    AnalogDigitalConverter adc12 = AnalogDigitalConverter(INTERNAL_TEMPERATURE_SENSOR_PIN, 30.0, -CALADC12_15V_30C, degC_per_bit);

    uart_config(bps9600);

	while(true){

        while(!on) {
            if (!(P1IN & BIT2)) {

                on = true;
                uart_writeline("on\n");

            }
        }

        float temp = adc12.perform_scaled_measure();

        char temp_str[40];
        //sprintf(temp_str, "%d,%0.2d\n", (int)temp, (int)(temp*10)%10);
        sprintf(temp_str, "%.1f\n", temp);
        uart_write(temp_str, strlen(temp_str));

        wait(5000);

        if (P1IN & BIT2) {
            
            on = false;
            uart_writeline("off\n");

        }

	}
    

    return 0;
}

//Switch 1
#pragma vector = PORT2_VECTOR
__interrupt void p2isr() {

    int i;
    unsigned long int delay;
    for(i=35; i>0; i--)
                    for(delay=10000000; delay>0; delay--);;

    if(!(P2IN & BIT1) && on) {

        uart_writeline("max\n");

    }

    P2IFG &= ~BIT1;
}

//Switch 2 + On/Off
#pragma vector = PORT1_VECTOR
__interrupt void p1isr() {

    int i;
    unsigned long int delay;
    for(i=35; i>0; i--)
                for(delay=10000000; delay>0; delay--);;

    if(!(P1IN & BIT1) && on) {

        uart_writeline("min\n");

    }

    P1IFG &= ~BIT1;
}
