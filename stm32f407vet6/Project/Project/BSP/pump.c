#include "pump.h"

/**
  * @brief  ���ÿ��ƺ���
  * @param  
  * @retval ��
  */
void pump_control(uint8_t state)
{
	if(state == 0)
	{
		__HAL_TIM_SetCompare(&htim4, TIM_CHANNEL_1, 500);
	}
	else if(state != 0)
	{
		__HAL_TIM_SetCompare(&htim4, TIM_CHANNEL_1, 2500);
	}
}

/**
  * @brief  ��ŷ����ƺ���
  * @param  
  * @retval ��
  */
void valve_control(uint8_t state)
{
	if(state == 0)
	{
		__HAL_TIM_SetCompare(&htim4, TIM_CHANNEL_2, 500);
	}
	else if(state != 0)
	{
		__HAL_TIM_SetCompare(&htim4, TIM_CHANNEL_2, 2500);
	}
}
