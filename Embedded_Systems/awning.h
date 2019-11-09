/*
 * awning.h
 *
 * Created: 8-11-2019 22:34:44
 *  Author:JGAR-IT
 */ 


#ifndef AWNING_H_
#define AWNING_H_


void upDownAwning();					


// Variables
uint16_t analog_value;						
uint16_t analog_echo;						
char temperature_sensor[5];					
char light_sensor[5];						
char distance_sensor[10];				


#endif /* AWNING_H_ */