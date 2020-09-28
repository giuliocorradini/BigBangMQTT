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

int main(void) {
    WDTCTL = WDTPW | WDTHOLD;

    P1DIR |= BIT0;

    timer_start();
    __enable_interrupt();

    int bits30 = CALADC12_15V_30C;
    int bits85 = CALADC12_15V_85C;
    float degC_per_bit = 55.0f/(float)(bits85-bits30);   //conversion slope

    AnalogDigitalConverter adc12 = AnalogDigitalConverter(INTERNAL_TEMPERATURE_SENSOR_PIN, 30.0, -CALADC12_15V_30C, degC_per_bit);

    uart_global_config(bps9600);
    UART uart;
    uart_init(&uart);

	while(true){

        float temp = adc12.perform_scaled_measure();

        char temp_str[40];
        //sprintf(temp_str, "%d,%0.2d\n", (int)temp, (int)(temp*10)%10);
        sprintf(temp_str, "%.1f\n", temp);
        uart.write((uint8_t*)temp_str, strlen(temp_str));

        wait(5000);

	}
    

    return 0;
}