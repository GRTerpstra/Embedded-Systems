/*
 *	awning.c
 *
 *	Created: 8-11-2019 22:33:54
 *  Author: JGAR-IT
 */

#include <avr/io.h>
#include <stdlib.h>
#define F_CPU 16E6
#include <util/delay.h>
#include <avr/interrupt.h>

#include "awning.h"
#include "sensors.h"
#include "serial.h"

// variables
uint16_t analog_value;						// Reads the analog value
uint16_t analog_echo;						// Reads the analog echo


char temperature_sensor[5];					// Value of the temperature sensor
char light_sensor[5];						// Value of light sensor
char distance_sensor[10];					// Value of distance sensor


int temperature_awning_down = 23;					// Temperature at which the awning closes
int temperature_awning_up = 17;						// Temperature at which the awning opens
int light_awning_down = 60;							// Level of light at which the awning closes
int light_awning_up = 16;							// Level of light at which the awning opens
int distance_awning_up = 40;						// Distance at which the awning opens
int distance_awning_down = 5;						// Distance at which the awning closes
int manual_awning_distance = 0;						// Manual set distance where awning closes

int manualMode = 0;									// If system is in manual mode


void upDownAwning()
{
	int sensor_light = atoi(light_sensor);					// Convert light sensor value to int and set ls
	int sensor_temperature = atoi(temperature_sensor);				// Convert temperature sensor value to int and set ts
	distanceStill();								// Get distance
	int sensor_distance = atoi(distance_sensor);					// Convert distance sensor value to int
	
	
	if(sensor_light >= light_awning_down || sensor_temperature >= temperature_awning_down)
	{
		PORTB &= ~(1 << PB5);						// Green LED off
		PORTB |= (1 << PB3);						// Red LED on
		
		
		if (sensor_distance > distance_awning_down)						// Makes yellow LED blink
		{
			PORTB |= (1 << PB4);
			_delay_ms(100);
			PORTB &= ~(1 << PB4);
			_delay_ms(100);
		}
	}
	else if(sensor_light <= light_awning_up || sensor_temperature <= temperature_awning_up )
	{
		PORTB &= ~(1 << PB3);
		PORTB |= (1 << PB5);
		
		
		if (sensor_distance < distance_awning_up)
		{
			PORTB |= (1 << PB4);
			_delay_ms(100);
			PORTB &= ~(1 << PB4);
			_delay_ms(100);
		}
	}
	
}

int unsigned combine(unsigned x, unsigned y)
{
	unsigned pow = 10;
	return (y * pow) + x;
}

int unsigned combine3(unsigned x, unsigned y, unsigned z)
{
	unsigned pow1 = 10;
	unsigned pow2 = 100;
	return (z * pow2) + (y * pow1) + x;
}

ISR ( USART_RX_vect )
{
	unsigned char ReceivedByte;
	ReceivedByte = UDR0;						// Set ReceivedByte to the received byte from the controller (GUI)
	
	switch(ReceivedByte)
	{
		case '1':								// 1 = Shut the sunshade // Red
		manualMode = 1;
		manual_awning_distance = 0;
		return;
		
		case '2':								// 2 = Open the sunshade // Green
		manualMode = 1;
		manual_awning_distance = 1;
		return;
		
		case '3':								// 3 = set
		manualMode = 0;
		temperature_awning_down = combine((int) USART_receive(), (int) USART_receive());
		temperature_awning_up = combine((int) USART_receive(), (int) USART_receive());
		light_awning_down = combine((int) USART_receive(), (int) USART_receive());
		light_awning_up = combine((int) USART_receive(), (int) USART_receive());
		return;
		
		case '7':								// 7 = open/closing distance
		manualMode = 1;
		int closeopen = combine3((int) USART_receive(), (int) USART_receive(), (int) USART_receive());
		distance_awning_up = closeopen;
		return;
		
		case '8':								// 8 = set manual ON / OFF
		manualMode = (int) USART_receive();		// 1/0
		if (manualMode == 1)					// manual mode on
		{
			manual_awning_distance = (int)atoi(distance_sensor);
		}
		return;
		
		default:
		return;
	}
}


