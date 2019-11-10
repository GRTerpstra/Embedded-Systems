/*
 * init.c
 *
 * Created: 7-11-2019 21:36:43
 * Author:JGAR-IT
 * Bron: https://sites.google.com/site/qeewiki/books/avr-guide/analog-input
 */ 

#include <stdlib.h>
#include <avr/interrupt.h>
#define F_CPU 16000000UL

#include "AVR_TTC_scheduler.h"
#include "awning.h"
#include "sensors.h"
#include "serial.h"

#define BAUDRATE 19200					// set the baudrate
#define BAUD_PRESCALLER (((F_CPU / (BAUDRATE * 16UL))) - 1)

void init_serial_connectie()
{
	UCSR0A = 0;							// disable U2X mode
	UCSR0C = (1<<USBS0)|(3<<UCSZ00);	// Set frame format: 8data, 2stop bit
}

void init_USART()
{
	UBRR0H = (uint8_t)(BAUD_PRESCALLER>>8);
	UBRR0L = (uint8_t)(BAUD_PRESCALLER);
	UCSR0B = (1<<RXEN0)|(1<<TXEN0);		// Enable receiver and transmitter
	UCSR0C = (3<<UCSZ00);
	UCSR0B |= (1 << RXCIE0 );			
								
}

void init_ttc_scheduler()
{
	SCH_Init_T1();					//Set up scheduler
	SCH_Add_Task(temperature,1,50); //Add 'temperature' task
	SCH_Add_Task(light,2,50);		//Add 'light' task
	SCH_Add_Task(distance,3,50);	//Add 'distance' task
	SCH_Add_Task(nextLine,4,50);	//Add 'nextline' task
	SCH_Add_Task(upDownAwning,0,25);//Add 'updown' task
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