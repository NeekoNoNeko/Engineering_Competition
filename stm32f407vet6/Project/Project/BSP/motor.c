#include "motor.h"
/*此为开环速度控制模式*/

/* 接线示意图
 * 				   TB6612
 * TIM3_CH3 ------ PWMA	VM  ------12V
 * GPIO3   ------ AIN2	VCC ------3.3V/5V
 * GPIO2   ------ AIN1	GND ------GND
 * 3.3V/5V ------ STBY	AO1 ------电机线+
 * 				  BIN1	AO2 ------电机线-
 * 				  BIN2	BO2
 * 				  PWMB	BO1
 * 				  GND	GND
 */

/**
  * @brief  设置TIM3通道3PWM值
  * @param  pwm值，范围 0~100
  * @retval 无
  */
void PWM_TIM3CH3_SetCompare(uint16_t Copmare)
{
	__HAL_TIM_SetCompare(&htim3, TIM_CHANNEL_3, Copmare);
}

/**
  * @brief  设置电机速度
  * @param  Speed设置电机的速度，范围 -100~100
  * @retval 无
  */
void Motor_SetSpeed(int8_t Speed)
{
	if(Speed >= 0)		//设置正转速度
	{
		HAL_GPIO_WritePin(GPIOC, GPIO_PIN_4, GPIO_PIN_SET);
		HAL_GPIO_WritePin(GPIOC, GPIO_PIN_5, GPIO_PIN_RESET);
		PWM_TIM3CH3_SetCompare(Speed);
	}
	else				//设置反转速度
	{
		HAL_GPIO_WritePin(GPIOC, GPIO_PIN_4, GPIO_PIN_RESET);
		HAL_GPIO_WritePin(GPIOC, GPIO_PIN_5, GPIO_PIN_SET);
		PWM_TIM3CH3_SetCompare(-Speed);
	}
}


