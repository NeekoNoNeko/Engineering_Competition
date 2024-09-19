#ifndef __SERVO_H__
#define __SERVO_H__

#include "tim.h"
#include "delay.h"
#include <math.h>

void Servo_SetAngle(float Angle, uint8_t Channel);
void Servo_SetAngle_Speed(float Angle, uint16_t Speed, uint8_t Channel);

#endif
