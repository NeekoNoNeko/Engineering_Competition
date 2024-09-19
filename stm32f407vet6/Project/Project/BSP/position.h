#ifndef __POSITION_H__
#define __POSITION_H__

/*
 * 四头丝杆，旋转一圈走0.8cm
 * 张大头步进电机一圈3200脉冲数
 * 所以 0.8/3200 = 0.00025cm，即 步进电机 1 脉冲数，走0.00025cm
 */

#include "main.h"
#include "Emm_V5.h"
#include "delay.h"
#include <math.h>

#define Step			0.1		//丝杆步长（精度），单位cm
#define Step_Pulse		400		//丝杆移动0.1cm所需要的脉冲数
#define Offset_X		0		//X轴定位偏移量，单位cm
#define Offset_Y		0		//Y轴定位偏移量，单位cm
#define Offset_Z		0		//Z轴定位偏移量，单位cm
#define Offset_Clamp	0		

#define Plate_HolePitch 4.0f			//药盘孔间距，单位cm

void X_Emm_V5_position(float x, uint16_t velocity);
void Y_Emm_V5_position(float y, uint16_t velocity);
void Z_Emm_V5_position(float z, uint16_t velocity);
void Clamp_Emm_V5_position(float clamp, uint16_t velocity, uint8_t accelerated_speed);
void XYZ_Return_Origin(uint8_t Mode);

void Plate_HolePitch_position(void);
void Tray_position(void);

bool z_arrive_check(void);
bool x_arrive_check(void);
bool y_arrive_check(void);

#endif
