/*
 * serial.c
 *
 * Created: 09-11-2019 16:35:55
 *  Author: JGAR-IT
 * Bron: https://www.avrfreaks.net/forum/atemga32u4-using-usart-solved
 */ 

#include <avr/io.h>
#include <stdlib.h>
#define F_CPU 16E6
#include <util/delay.h>

void sendData(){
	
}

unsigned char USART_receive(void)
{   //wait for data to be received
	loop_until_bit_is_set(UCSR0A,RXC0);
	//get and return received data from buffer
	return UDR0;
}

void USART_transmit(unsigned char data)
{	// Wait for empty transmit buffer
	loop_until_bit_is_set(UCSR0A, UDRE0);
	//puts data into buffer, sends the data
	UDR0 = data;
}

void USART_putstring(char* StringPtr)
{
	while(*StringPtr != 0x00){       //check if there is still more chars send, this is done checking the actual char and see if it is different from the null char
		USART_transmit(*StringPtr);  // Using the simple send function we send one char at a time
	StringPtr++;}                    // Increment the pointer, so the next char can be read
}

void nextLine()
{
	USART_transmit('\r');			  //Set the new line to the begin of the page
	USART_transmit('\n');			  //Go to next line
}

uint16_t read_analog(uint8_t value)
{
	ADMUX &= 0xF0;                      //Clear the older channel that was read
	ADMUX |= value;                     //Defines the new analog channel to be read
	ADCSRA |= (1 << ADSC);              //Starts a new calculation
	while(ADCSRA & (1 << ADSC));        //Wait until the calculation is done
	return ADCW;						//Returns the analog value of the selected channel
}