/*
 * init.c
 *
 * Created: 7-11-2019 23:56:11
 * Author:JGAR-IT
 * Temperature Sensor (TMP36) connect with analog in port 0
 * Light Sensor(LDR) connect with analog in port 1
 * Ultrasonic Sensor(HC-SR04) the echo pin is connect with PIND6
 * Ultrasonic Sensor(HC-SR04) the trig pin is connect with PIND7
 * PIN11 : Red LED
 * PIN12 : Yellow LED
 * PIN13 : Green LED
 */

#include <avr/io.h>
#define F_CPU 16000000UL
#include <util/delay.h>

#include "AVR_TTC_scheduler.h"
#include "init.h"


void setup()
{
	init_serial_connectie();
	init_analog();				// Setup the ADC
	init_USART();				// Setup the USART
	init_distance();			// Setup distance sensor
	init_ttc_scheduler();		// Setup scheduler
	init_LEDS();				// Setup LED
	_delay_ms(100);				// Half second delay to initialize everything
}

int main(void)
{
	setup();
	while(1) {
		SCH_Dispatch_Tasks();
	}
}