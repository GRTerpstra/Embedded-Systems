/*
 * sensors.c
 *
 * Created: 7-11-2019 18:06:25
 *  Author: JGAR-IT
 */ 
#include <avr/io.h>
#include <stdlib.h>
#define F_CPU 16000000UL
#include <util/delay.h>
#include "awning.h"
#include "sensors.h"
#include "serial.h"

void temperature()
{
	USART_putstring(" Temperature : ");
	analog_value = read_analog(0);
	analog_value = (((((double)analog_value / 1024) * 5) - 0.5) * 100);		 // Calculate temperature
	itoa(analog_value, temperature_sensor, 10);								//  Convert the read value to an ascii string
	USART_putstring(temperature_sensor);								   //   Send the converted value to the terminal
	USART_putstring("  ");
}

void light()
{
	USART_putstring(" Light : ");
	analog_value = read_analog(1);
	analog_value = ((((double)analog_value)/1024)*100 *1.5);			  // Calculate the amount of light
	itoa(analog_value, light_sensor, 10);							  // Convert the read value to an ascii string
	USART_putstring(light_sensor);								  // Send the converted value to the terminal
	
}

void distance()
{
	OCR1A = 0x640;								
	USART_putstring(" Distance : ");
	PORTD |= (1<< PD7);
	_delay_us(10);
	PORTD &= ~(1 << PD7);							// Give pulse from 10us
	
	loop_until_bit_is_set(PIND, PD6);
	TCNT1 = 0;
	loop_until_bit_is_clear(PIND, PD6);
	uint16_t count = TCNT1;
	float distance = ((float)count / 4);		// Calculate the distance

	itoa(distance, distance_sensor, 10);        // Convert the read value to an ascii string
	USART_putstring(distance_sensor);			// Send the converted value to the terminal
	USART_putstring("  ");
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