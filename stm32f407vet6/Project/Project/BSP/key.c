#include "key.h"

/* key硬件电路结构
 *
 * GPIO------key-----
 *					|
 *					|
 *				   GND
 */

void key_init(void)
{
	GPIO_InitTypeDef GPIO_InitStruct = {0};
	
	__HAL_RCC_GPIOB_CLK_ENABLE();
	__HAL_RCC_GPIOE_CLK_ENABLE();
	
	/*PB8,PB9*/
	GPIO_InitStruct.Pin = GPIO_PIN_8|GPIO_PIN_9;
	GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
	GPIO_InitStruct.Pull = GPIO_PULLUP;
	HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);
	
	/*PE0,PE1*/
	GPIO_InitStruct.Pin = GPIO_PIN_0|GPIO_PIN_1;
	GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
	GPIO_InitStruct.Pull = GPIO_PULLUP;
	HAL_GPIO_Init(GPIOE, &GPIO_InitStruct);
}

uint8_t key_num(void)
{
	uint8_t num;
	
	//key1(SW3)
	if(HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_9) == 0)		//按下低电平
	{
		delay_ms(20);
		while(HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_9) == 0);
		delay_ms(20);
		num = 1;
	}
	//key2(SW5)
	else if(HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_8) == 0)
	{
		delay_ms(20);
		while(HAL_GPIO_ReadPin(GPIOB, GPIO_PIN_8) == 0);
		delay_ms(20);
		num = 2;
	}
	//key3(SW4)
	else if(HAL_GPIO_ReadPin(GPIOE, GPIO_PIN_0) == 0)
	{
		delay_ms(20);
		while(HAL_GPIO_ReadPin(GPIOE, GPIO_PIN_0) == 0);
		delay_ms(20);
		num = 3;
	}
	//key4(SW6)
	else if(HAL_GPIO_ReadPin(GPIOE, GPIO_PIN_1) == 0)
	{
		delay_ms(20);
		while(HAL_GPIO_ReadPin(GPIOE, GPIO_PIN_1) == 0);
		delay_ms(20);
		num = 4;
	}
	
	return num;
}
