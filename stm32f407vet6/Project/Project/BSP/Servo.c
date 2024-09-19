#include "Servo.h"

/*
 *	ע�⣺δ��д��ת�������룬��Ҫ�����д
 * 	��ת����˼·����if�Ѷ�����Ƕ����úã��������Ƕ�Ӧ����ô�����ǻص���㻹��ά�����Ƕ�
 *		��ת����������1.ADC��������С������һ��ֵ��PWM�ź�����Ϊ��Сֵ
 *					  2.�����ⷨ��ʹ�ö�ʱ����ʱ������һ��ʱ����δ����ָ��λ�ã���PWM�ź�����Ϊ��Сֵ
 */


/**
  * @brief  ���ö���Ƕȣ�180�ȶ����
  * @param  Angle������õĽǶȣ�0~180
  * @retval ��
  */
void Servo_SetAngle(float Angle, uint8_t Channel)
{
	uint16_t angle_pwm = 0;
	
	/*���ƴ�С*/
//	if(Angle > 180)	{Angle = 180;}
//	if(Angle < 0)	{Angle = 0;}
	
	angle_pwm = round(Angle / 180 * 2000) + 500;		//ARR�������20k��20k�൱��20ms
	
	switch(Channel)
	{
		case 1:
		{
			__HAL_TIM_SetCompare(&htim4, TIM_CHANNEL_1, angle_pwm);
		}break;
		case 2:
		{
			__HAL_TIM_SetCompare(&htim4, TIM_CHANNEL_2, angle_pwm);
		}break;
		case 3:
		{
			__HAL_TIM_SetCompare(&htim4, TIM_CHANNEL_3, angle_pwm);
		}break;
	}
}

/**
  * @brief  ���ö���ǶȺ��ٶȣ�180�ȶ����
  *	˵��������������ֵֻ��ӽ������Ƕ�
  * @param  Angle������õĽǶȣ���Χ 0~180
  * @param  Speed������õ��ٶȣ�ֵԽС�ٶ�Խ��
  * @retval ��
  */
void Servo_SetAngle_Speed(float Angle, uint16_t Speed, uint8_t Channel)
{
	float angle_pwm = 0;
	angle_pwm = Angle / 180 * 2000 + 500;		//ARR�������20k��20k�൱��20ms
	
	for(uint16_t i = 0; i < angle_pwm; i += Speed)
	{
		if(Channel == 1)
		{
			__HAL_TIM_SetCompare(&htim4, TIM_CHANNEL_1, i);
		}
		else if(Channel == 2)
		{
			__HAL_TIM_SetCompare(&htim4, TIM_CHANNEL_2, i);
		}
		else if(Channel == 3)
		{
			__HAL_TIM_SetCompare(&htim4, TIM_CHANNEL_3, i);
		}
		delay_ms(15);
	}
}

