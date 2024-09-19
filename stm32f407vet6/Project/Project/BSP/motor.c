#include "motor.h"
/*��Ϊ�����ٶȿ���ģʽ*/

/* ����ʾ��ͼ
 * 				   TB6612
 * TIM3_CH3 ------ PWMA	VM  ------12V
 * GPIO3   ------ AIN2	VCC ------3.3V/5V
 * GPIO2   ------ AIN1	GND ------GND
 * 3.3V/5V ------ STBY	AO1 ------�����+
 * 				  BIN1	AO2 ------�����-
 * 				  BIN2	BO2
 * 				  PWMB	BO1
 * 				  GND	GND
 */

/**
  * @brief  ����TIM3ͨ��3PWMֵ
  * @param  pwmֵ����Χ 0~100
  * @retval ��
  */
void PWM_TIM3CH3_SetCompare(uint16_t Copmare)
{
	__HAL_TIM_SetCompare(&htim3, TIM_CHANNEL_3, Copmare);
}

/**
  * @brief  ���õ���ٶ�
  * @param  Speed���õ�����ٶȣ���Χ -100~100
  * @retval ��
  */
void Motor_SetSpeed(int8_t Speed)
{
	if(Speed >= 0)		//������ת�ٶ�
	{
		HAL_GPIO_WritePin(GPIOC, GPIO_PIN_4, GPIO_PIN_SET);
		HAL_GPIO_WritePin(GPIOC, GPIO_PIN_5, GPIO_PIN_RESET);
		PWM_TIM3CH3_SetCompare(Speed);
	}
	else				//���÷�ת�ٶ�
	{
		HAL_GPIO_WritePin(GPIOC, GPIO_PIN_4, GPIO_PIN_RESET);
		HAL_GPIO_WritePin(GPIOC, GPIO_PIN_5, GPIO_PIN_SET);
		PWM_TIM3CH3_SetCompare(-Speed);
	}
}


