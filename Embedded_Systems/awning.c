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


int temperature_awning_down = 23;							// Temperature at which the awning closes
int temperature_awning_up = 17;							// Temperature at which the awning opens
int light_awning_down = 60;							// Level of light at which the awning closes
int light_awning_up = 16;							// Level of light at which the awning opens
int distance_awning_up = 40;						// Distance at which the awning opens
int distance_awning_down = 5;						// Distance at which the awning closes


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


