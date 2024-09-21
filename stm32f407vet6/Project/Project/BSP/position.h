#ifndef __POSITION_H__
#define __POSITION_H__

/*
 * ��ͷ˿�ˣ���תһȦ��0.8cm
 * �Ŵ�ͷ�������һȦ3200������
 * ���� 0.8/3200 = 0.00025cm���� ������� 1 ����������0.00025cm
 */

#include "main.h"
#include "Emm_V5.h"
#include "delay.h"
#include <math.h>

#define Step			0.1		//˿�˲��������ȣ�����λcm
#define Step_Pulse		400		//˿���ƶ�0.1cm����Ҫ��������
#define Offset_X		0		//X�ᶨλƫ��������λcm
#define Offset_Y		0		//Y�ᶨλƫ��������λcm
#define Offset_Z		0		//Z�ᶨλƫ��������λcm
#define Offset_Clamp	0		

#define Plate_HolePitch 4.0f			//ҩ�̿׼�࣬��λcm

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
