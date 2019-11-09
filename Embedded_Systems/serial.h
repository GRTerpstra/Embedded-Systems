/*
 * serial.h
 *
 * Created: 10-11-2019 18:16:37
 *  Author: JGAR-IT
 */ 


#ifndef SERAIL_H_
#define SERAIL_H_


unsigned char USART_receive(void);		
void USART_transmit(unsigned char data);	
void USART_putstring(char* StringPtr);	
void nextLine();							
uint16_t read_analog(uint8_t channel);     

#endif /* SERAIL_H_ */