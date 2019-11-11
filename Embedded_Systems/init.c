/*
 * init.c
 *
 * Created: 7-11-2019 21:36:43
 * Author:JGAR-IT
 * Bron: https://sites.google.com/site/qeewiki/books/avr-guide/analog-input
 */ 

#include <stdlib.h>
#include <avr/interrupt.h>
#define F_CPU 16E6

#include "AVR_TTC_scheduler.h"
#include "awning.h"
#include "sensors.h"
#include "serial.h"

#define UBBRVAL 51



void init_USART()
{
	/* Set baud rate */
	UBRR0H = 0;
	UBRR0L = UBBRVAL;
	/* Enable receiver and transmitter */
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);
	/* Set frame format: 8data, 1stop bit */
	UCSR0C = (1<<UCSZ01) |(1<<UCSZ00);
}

void init_ttc_scheduler()
{
	SCH_Init_T1();					//Set up scheduler
	SCH_Add_Task(temperature,1,100); //Add 'temperature' task
	SCH_Add_Task(light,2,100);		//Add 'light' task
	SCH_Add_Task(distance,3,100);	//Add 'distance' task
	SCH_Add_Task(putString,4,50);	//Add 'putString' task
	//SCH_Add_Task(upDownAwning,0,25);//Add 'updown' task
	SCH_Start();					//Start running the scheduler 
}

void init_analog()
{
	ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));    // 16Mhz/128 = 125Khz the ADC reference clock
	ADMUX |= (1<<REFS0);							 // Voltage reference from AVCC (5v)
	ADCSRA |= (1<<ADEN);							 // Turn on ADC
	ADCSRA |= (1<<ADSC);							 // Do an initial conversion because this one is the slowest and to ensure that everything is up and running
}

void init_distance()
{
	DDRD |= (1<< PD7);			// Pin 3 Trigger Output
	DDRD &= ~(1 << PD6);		// Pin 2 Echo Input
}

void init_LEDS()
{
	DDRB |= (1 <<PB3);			// pin0 B = output
	DDRB |= (1 << PB4);			// pin1 B = output
	DDRB |= (1 << PB5);			// pin2 B = output
	PORTB |= (1 << PB5);		// Green LED on
}