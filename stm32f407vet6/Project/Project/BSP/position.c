#include "position.h"

/*X������*/
//float last_x;
//uint32_t x_pulse;
//uint32_t last_x_pulse;
//uint8_t dir_x;

/*Y������*/
//float last_y;
//uint32_t y_pulse;
//uint32_t last_y_pulse;
//uint8_t dir_y;

/*Z������*/
//float last_z;
//uint32_t z_pulse;
//uint32_t last_z_pulse;
//uint8_t dir_z;

/*����������Ϊ���½ṹ��*/
struct CSYS
{
	float last_coord;			//�ϴ�����
	uint32_t pulse;				//����
	uint32_t last_pulse;		//�ϴ�����
	uint8_t dir;				//�����������Χ 0~1 ��0Ϊ��ת��1Ϊ��ת
}X, Y, Z, Clamp;

__IO uint8_t j = 0;
/*�����ϸ���Ʒλ�ã�ҩ�塢ҩƿ������*/
extern __IO float plate_x, plate_y;			//ҩ��λ��
extern __IO float tray_x, tray_y;			//����λ��

extern __IO uint16_t Emm_speed;		//42������������ٶ�
extern __IO uint8_t Emm_Z_acc;		//Z�������ٶ�

/*��������λ�����У�z������ȼ�Ӧ��Ҫ����ߵģ�����z��û�е���ָ��λ��ǰ��x���y�᲻���ж���*/
__IO bool z_arriveflag = false;			//z�ᵽλ��־λ
__IO bool x_arriveflag = false;			//x�ᵽλ��־λ
__IO bool y_arriveflag = false;			//y�ᵽλ��־λ


/*****************************************************************************************************/

/**
  * @brief  X�ᶨλ
  * @param  x��X�ᶨλ���꣬��Χ 0~49����λcm
  * @param	velocity������ٶ�
  * @retval ��
  */
void X_Emm_V5_position(float x, uint16_t velocity)
{
//	x_arriveflag = false;
	
	X.pulse = round((double)(x + Offset_X) / Step * Step_Pulse);
	X.last_pulse = round((double)(X.last_coord + Offset_X) / Step * Step_Pulse);
	
	/*�����ж�*/
	if(x < X.last_coord)	//�µ�Ⱦɵ�С����ʼ�ɵ����������Ϊ0
	{
		X.dir = 0;		//��ת
		X.pulse = X.last_pulse - X.pulse;
	}
	else if(x > X.last_coord)
	{
		X.dir = 1;		//��ת
		X.pulse = X.pulse - X.last_pulse;
	}
	else if(x == X.last_coord)
	{
		X.dir = 1;
		X.pulse = 0;
	}
	
	Emm_V5_Pos_Control(1, X.dir, velocity, 0, X.pulse, 0, 0, 1);		//1�ŵ����X������
	/*�ȴ���������������ݻ���������rxCmd�ϣ�����ΪrxCount*/
	while(usart1_rxFrameFlag == false);
	usart1_rxFrameFlag = false;
	
	X.last_coord = x;
	
	/*��λ�ж�*/
//	while(1)
//	{
//		if(usart1_rxCmd[0] == 0x01 && usart1_rxCmd[3] == 0x6B && usart1_rxCount == 4)
//		{
//			if(usart1_rxCmd[1] == 0xFD && usart1_rxCmd[2] == 0x9F)
//			{
//				OLED_ShowString(0, 40, "arr_x", OLED_6X8);
//				OLED_Update();
//				break;
//			}
//		}
//	}
}

/**
  * @brief  Y�ᶨλ
  * @param  y��Y�ᶨλ���꣬��Χ 0~26����λcm
  * @param	velocity������ٶ�
  * @retval ��
  */
void Y_Emm_V5_position(float y, uint16_t velocity)
{
//	y_arriveflag = false;
	
	Y.pulse = round((double)(y + Offset_Y) / Step * Step_Pulse);
	Y.last_pulse = round((double)(Y.last_coord + Offset_Y) / Step * Step_Pulse);
	
	/*�����ж�*/
	if(y < Y.last_coord)	//�µ�Ⱦɵ�С����ʼ�ɵ����������Ϊ0
	{
		Y.dir = 0;		//��ת
		Y.pulse = Y.last_pulse - Y.pulse;
	}
	else if(y > Y.last_coord)
	{
		Y.dir = 1;		//��ת
		Y.pulse = Y.pulse - Y.last_pulse;
	}
	else if(y == Y.last_coord)
	{
		Y.dir = 1;
		Y.pulse = 0;
	}
	
	Emm_V5_Pos_Control(1, Y.dir, velocity, 0, Y.pulse, 0, 0, 2);		//2�ŵ����Y������
	/*�ȴ���������������ݻ���������rxCmd�ϣ�����ΪrxCount*/
	while(usart2_rxFrameFlag == false);
	usart2_rxFrameFlag = false;
	
	Y.last_coord = y;
	
	/*��λ�ж�*/
//	while(1)
//	{
//		if(usart2_rxCmd[0] == 0x01 && usart2_rxCmd[3] == 0x6B && usart2_rxCount == 4)
//		{
//			if(usart2_rxCmd[1] == 0xFD && usart2_rxCmd[2] == 0x9F)
//			{
//				OLED_ShowString(36, 40, "arr_y", OLED_6X8);
//				OLED_Update();
//				break;
//			}
//		}
//	}
}

/**
  * @brief  Z�ᶨλ
  * @param  z��Z�ᶨλ���꣬��Χ 0~18����λcm
  * @param	velocity������ٶ�
  * @retval ��
  */
void Z_Emm_V5_position(float z, uint16_t velocity)
{
//	z_arriveflag = false;
	
	Z.pulse = round((double)(z + Offset_Z) / Step * Step_Pulse);
	Z.last_pulse = round((double)(Z.last_coord + Offset_Z) / Step * Step_Pulse);
	
	/*�����ж�*/
	if(z < Z.last_coord)	//�µ�Ⱦɵ�С����ʼ�ɵ����������Ϊ0
	{
		Z.dir = 1;		//��ת
		Z.pulse = Z.last_pulse - Z.pulse;
	}
	else if(z > Z.last_coord)
	{
		Z.dir = 0;		//��ת
		Z.pulse = Z.pulse - Z.last_pulse;
	}
	else if(z == Z.last_coord)
	{
		Z.dir = 0;
		Z.pulse = 0;
	}
	
	Emm_V5_Pos_Control(1, Z.dir, velocity, Emm_Z_acc, Z.pulse, 0, 0, 4);		//4�ŵ����Z������
	/*�ȴ���������������ݻ���������rxCmd�ϣ�����ΪrxCount*/
	while(uart4_rxFrameFlag == false);
	uart4_rxFrameFlag = false;
	
	Z.last_coord = z;
	
	/*��λ�ж�*/
//	while(1)
//	{
//		if(uart4_rxCmd[0] == 0x01 && uart4_rxCmd[3] == 0x6B && uart4_rxCount == 4)
//		{
//			if(uart4_rxCmd[1] == 0xFD && uart4_rxCmd[2] == 0x9F)
//			{
//				OLED_ShowString(72, 40, "arr_z", OLED_6X8);
//				OLED_Update();
//				break;
//			}
//		}
//	}
}

/**
  * @brief  ҩƿ�Ƽ��гֵ�����뺯��
  * @param  clamp���ӳ��ƶ����룬��Χ 0~10.3����λcm
  * @param	velocity������ٶ�
  * @param	accelerated_speed��������ٶ�
  * @retval ��
  */
void Clamp_Emm_V5_position(float clamp, uint16_t velocity, uint8_t accelerated_speed)
{
	Clamp.pulse = round((double)(clamp + Offset_Clamp) / Step * Step_Pulse);
	Clamp.last_pulse = round((double)(Clamp.last_coord + Offset_Clamp) / Step * Step_Pulse);
	
	/*�����ж�*/
	if(clamp < Clamp.last_coord)	//�µ�Ⱦɵ�С����ʼ�ɵ����������Ϊ0
	{
		Clamp.dir = 1;		//��ת
		Clamp.pulse = Clamp.last_pulse - Clamp.pulse;
	}
	else if(clamp > Clamp.last_coord)
	{
		Clamp.dir = 0;		//��ת
		Clamp.pulse = Clamp.pulse - Clamp.last_pulse;
	}
	else if(clamp == Clamp.last_coord)
	{
		Clamp.dir = 1;
		Clamp.pulse = 0;
	}
	
	Emm_V5_Pos_Control(1, Clamp.dir, velocity, accelerated_speed, Clamp.pulse, 0, 0, 3);		//3�ŵ����ҩƿ�Ƽ��гֵ����
	/*�ȴ���������������ݻ���������rxCmd�ϣ�����ΪrxCount*/
	while(usart3_rxFrameFlag == false);
	usart3_rxFrameFlag = false;
	
	Clamp.last_coord = clamp;
}


/*****************************************************************************************************/

/**
  * @brief  XYZ����㺯��
  * @param  Mode������ģʽ
  *			0 ��Ȧ�ͽ����㣻1 ��Ȧ������㣻2 ��Ȧ����λ��ײ���㣻3 ��Ȧ����λ���ػ���
  * @retval ��
  */
void XYZ_Return_Origin(uint8_t Mode)
{
//	/*z�������ز���*/
//	float z_up_cm = 10.0;	//z����������߶ȣ���λcm
//	uint32_t z_Orogin_up;	//z���������������
//	
//	z_Orogin_up = round((double)z_up_cm / Step * Step_Pulse);
//	
//	/*z����������߶ȣ���ֹײ�������ϵ���Ʒ����������10cm*/
//	Emm_V5_Pos_Control(1, 0, 100, 0, z_Orogin_up, 0, 0, 3);
//	/*�ȴ���������������ݻ���������rxCmd�ϣ�����ΪrxCount*/
//	while(rxFrameFlag == false);
//	rxFrameFlag = false;
	
	/*X�����*/
	Emm_V5_Origin_Trigger_Return(1, Mode, 0, 1);
	/*�ȴ���������������ݻ���������rxCmd�ϣ�����ΪrxCount*/
	while(usart1_rxFrameFlag == false);
	usart1_rxFrameFlag = false;
	
	/*Y�����*/
	Emm_V5_Origin_Trigger_Return(1, Mode, 0, 2);
	/*�ȴ���������������ݻ���������rxCmd�ϣ�����ΪrxCount*/
	while(usart2_rxFrameFlag == false);
	usart2_rxFrameFlag = false;
	
	/*Z�����*/
	Emm_V5_Origin_Trigger_Return(1, Mode, 0, 4);
	/*�ȴ���������������ݻ���������rxCmd�ϣ�����ΪrxCount*/
	while(uart4_rxFrameFlag == false);
	uart4_rxFrameFlag = false;
}


/*****************************************************************************************************/

/**
  * @brief  ҩ�̿�λ�ö�λ���ƶ�
  * @param  ��
  * @retval ��
  */
void Plate_HolePitch_position(void)
{
	j ++;
	switch(j)
	{
		case 1:		//��2��
		{
			plate_x += Plate_HolePitch;
		}break;
		case 2:		//��3��
		{
			plate_x += Plate_HolePitch;
		}break;
		case 3:		//��4��
		{
			plate_x = plate_x - Plate_HolePitch * 2;
			plate_y += Plate_HolePitch;
		}break;
		case 4:		//��5��
		{
			plate_x += Plate_HolePitch;
		}break;
		case 5:		//��6��
		{
			plate_x += Plate_HolePitch;
		}break;
	}
}

/**
  * @brief  ���̶�λ
  * @param  ��
  * @retval ��
  */
void Tray_position(void)
{
	Z_Emm_V5_position(12, Emm_speed);
	while(z_arrive_check() == false);
	
	X_Emm_V5_position(tray_x, Emm_speed);
	Y_Emm_V5_position(tray_y, Emm_speed);
	while(x_arrive_check() == false || y_arrive_check() == false);
}


/*****************************************************************************************************/

/**
  * @brief  z�ᵽλ���
  * @param  ��
  * @retval ��
  */
bool z_arrive_check(void)
{
	z_arriveflag = false;
	
	if(uart4_rxCmd[0] == 0x01 && uart4_rxCmd[3] == 0x6B && uart4_rxCount == 4)
	{
		if(uart4_rxCmd[1] == 0xFD && uart4_rxCmd[2] == 0x9F)
		{
			z_arriveflag = true;
		}
	}
	return z_arriveflag;
}

/**
  * @brief  x�ᵽλ���
  * @param  ��
  * @retval ��
  */
bool x_arrive_check(void)
{
	x_arriveflag = false;
	
	if(usart1_rxCmd[0] == 0x01 && usart1_rxCmd[3] == 0x6B && usart1_rxCount == 4)
	{
		if(usart1_rxCmd[1] == 0xFD && usart1_rxCmd[2] == 0x9F)
		{
			x_arriveflag = true;
		}
	}
	return x_arriveflag;
}

bool y_arrive_check(void)
{
	y_arriveflag = false;
	
	if(usart2_rxCmd[0] == 0x01 && usart2_rxCmd[3] == 0x6B && usart2_rxCount == 4)
	{
		if(usart2_rxCmd[1] == 0xFD && usart2_rxCmd[2] == 0x9F)
		{
			y_arriveflag = true;
		}
	}
	return y_arriveflag;
}

