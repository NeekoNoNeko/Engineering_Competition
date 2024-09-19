#include "Servo.h"

/*
 *	注意：未编写堵转保护代码，需要额外编写
 * 	堵转保护思路，用if把舵机最大角度设置好，超过最大角度应该怎么样，是回到零点还是维持最大角度
 *		堵转保护方案：1.ADC检测电流大小，超过一定值将PWM信号设置为最小值
 *					  2.经验检测法，使用定时器计时，超过一定时间电机未到达指定位置，则将PWM信号设置为最小值
 */


/**
  * @brief  设置舵机角度（180度舵机）
  * @param  Angle舵机设置的角度，0~180
  * @retval 无
  */
void Servo_SetAngle(float Angle, uint8_t Channel)
{
	uint16_t angle_pwm = 0;
	
	/*限制大小*/
//	if(Angle > 180)	{Angle = 180;}
//	if(Angle < 0)	{Angle = 0;}
	
	angle_pwm = round(Angle / 180 * 2000) + 500;		//ARR必须等于20k，20k相当于20ms
	
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
  * @brief  设置舵机角度和速度（180度舵机）
  *	说明：舵机最终输出值只会接近期望角度
  * @param  Angle舵机设置的角度，范围 0~180
  * @param  Speed舵机设置的速度，值越小速度越慢
  * @retval 无
  */
void Servo_SetAngle_Speed(float Angle, uint16_t Speed, uint8_t Channel)
{
	float angle_pwm = 0;
	angle_pwm = Angle / 180 * 2000 + 500;		//ARR必须等于20k，20k相当于20ms
	
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

