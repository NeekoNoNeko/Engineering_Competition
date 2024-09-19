#ifndef __PUMP_H__
#define __PUMP_H__

#include "stm32f4xx_hal.h"
#include "tim.h"

void pump_control(uint8_t state);
void valve_control(uint8_t state);

#endif
