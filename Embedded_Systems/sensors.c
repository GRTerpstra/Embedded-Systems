/*
 * sensors.c
 *
 * Created: 7-11-2019 18:06:25
 *  Author: JGAR-IT
 */ 
#include <avr/io.h>
#include <stdlib.h>
#define F_CPU 16E6
#include <util/delay.h>
#include "awning.h"
#include "sensors.h"
#include "serial.h"

char *values[] = {"0","0","0"};

void putString(){
	
	USART_putstring("{\"t\":");
	USART_putstring(values[0]);
	USART_putstring(",\"l\":");
	USART_putstring(values[1]);
	USART_putstring(",\"d\":");
	USART_putstring(values[2]);
	USART_putstring("}");
	
	nextLine();
}

void temperature()
{
	analog_value = read_analog(0);
	analog_value = (((((double)analog_value / 1024) * 5) - 0.5) * 100);		 // Calculate temperature
	itoa(analog_value, temperature_sensor, 10);								//  Convert the read value to an ascii string
	values[0] = temperature_sensor;
}

void light()
{
	analog_value = read_analog(1);
	analog_value = ((((double)analog_value)/1024)*100 *1.5);			  // Calculate the amount of light
	itoa(analog_value, light_sensor, 10);							  // Convert the read value to an ascii string
	values[1] = light_sensor;											// Send value to the terminal
}

void distance()
{
	OCR1A = 0x640;								
	PORTD |= (1<< PD7);
	_delay_us(10);
	PORTD &= ~(1 << PD7);							// Give pulse from 10us]]200000000000
	loop_until_bit_is_set(PIND, PD6);
	TCNT1 = 0;
	loop_until_bit_is_clear(PIND, PD6);
	uint16_t count = TCNT1;
	float distance = ((float)count / 4);		// Calculate the distance

	itoa(distance, distance_sensor, 10);        // Convert the read value to an ascii string
	values[2] = distance_sensor;

}

void distanceStill()
{
	OCR1A = 0x640;								
	PORTD |= (1 << PD7);
	_delay_us(10);
	PORTD &= ~(1<< PD7);							
	loop_until_bit_is_set(PIND, PD6);
	TCNT1 = 0;
	loop_until_bit_is_clear(PIND, PD6);
	uint16_t count = TCNT1;
	float distance = ((float)count / 4);		// Calculate the distance
	itoa(distance, distance_sensor, 10);        // Convert the read value to an ASCII string
}