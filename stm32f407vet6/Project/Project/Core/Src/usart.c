/**
  ******************************************************************************
  * @file    usart.c
  * @brief   This file provides code for the configuration
  *          of the USART instances.
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2024 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "usart.h"

/* USER CODE BEGIN 0 */

/*usart1，usart2，usart3，uart4为Emm_V5串口*/
/*uart5，usart6为视觉串口*/

#include "stdbool.h"
#include <stdint.h>
#include <stdio.h>

/*Emm_V5队列缓冲区参数*/
/*usart1*/
__IO bool usart1_rxFrameFlag = false;
__IO uint8_t usart1_rxCmd[FIFO_SIZE] = {0};
__IO uint8_t usart1_rxCount = 0;
/*usart2*/
__IO bool usart2_rxFrameFlag = false;
__IO uint8_t usart2_rxCmd[FIFO_SIZE] = {0};
__IO uint8_t usart2_rxCount = 0;
/*usart3*/
__IO bool usart3_rxFrameFlag = false;
__IO uint8_t usart3_rxCmd[FIFO_SIZE] = {0};
__IO uint8_t usart3_rxCount = 0;
/*uart4*/
__IO bool uart4_rxFrameFlag = false;
__IO uint8_t uart4_rxCmd[FIFO_SIZE] = {0};
__IO uint8_t uart4_rxCount = 0;

/*视觉参数*/
extern __IO float openmv_x, openmv_y;			//openmv坐标数据
extern __IO uint8_t openmv_colourflag_plate;	//openmv颜色标志位-药板
extern __IO uint8_t openmv_colourflag_bottle;	//openmv颜色标志位-药瓶
extern __IO uint8_t openmv_statusflag;			//openmv状态标志位
extern __IO uint8_t openmv_quadrantflag;		//openmv象限标志位

/*接收openmv发送的数据*/
uint8_t rx_openmv_buffer[11];
uint8_t rx_bufferIndex = 0;

/* USER CODE END 0 */

UART_HandleTypeDef huart4;
UART_HandleTypeDef huart5;
UART_HandleTypeDef huart1;
UART_HandleTypeDef huart2;
UART_HandleTypeDef huart3;

/* UART4 init function */
void MX_UART4_Init(void)
{

  /* USER CODE BEGIN UART4_Init 0 */

  /* USER CODE END UART4_Init 0 */

  /* USER CODE BEGIN UART4_Init 1 */

  /* USER CODE END UART4_Init 1 */
  huart4.Instance = UART4;
  huart4.Init.BaudRate = 115200;
  huart4.Init.WordLength = UART_WORDLENGTH_8B;
  huart4.Init.StopBits = UART_STOPBITS_1;
  huart4.Init.Parity = UART_PARITY_NONE;
  huart4.Init.Mode = UART_MODE_TX_RX;
  huart4.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart4.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart4) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN UART4_Init 2 */
  
  /*清除UART4的中断*/
  UART4->SR; UART4->DR;
  __HAL_UART_CLEAR_FLAG(&huart4, UART_FLAG_RXNE);
  
  /*使能UART4的中断*/
  __HAL_UART_ENABLE_IT(&huart4, UART_IT_RXNE);
  __HAL_UART_ENABLE_IT(&huart4, UART_IT_IDLE);

  /* USER CODE END UART4_Init 2 */

}
/* UART5 init function */
void MX_UART5_Init(void)
{

  /* USER CODE BEGIN UART5_Init 0 */

  /* USER CODE END UART5_Init 0 */

  /* USER CODE BEGIN UART5_Init 1 */

  /* USER CODE END UART5_Init 1 */
  huart5.Instance = UART5;
  huart5.Init.BaudRate = 9600;
  huart5.Init.WordLength = UART_WORDLENGTH_8B;
  huart5.Init.StopBits = UART_STOPBITS_1;
  huart5.Init.Parity = UART_PARITY_NONE;
  huart5.Init.Mode = UART_MODE_TX_RX;
  huart5.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart5.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart5) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN UART5_Init 2 */
  
  /*清除UART5的中断*/
  __HAL_UART_CLEAR_FLAG(&huart5, UART_FLAG_RXNE);
  
  /*使能UART5的中断*/
  __HAL_UART_ENABLE_IT(&huart5, UART_IT_RXNE);

  /* USER CODE END UART5_Init 2 */

}
/* USART1 init function */

void MX_USART1_UART_Init(void)
{

  /* USER CODE BEGIN USART1_Init 0 */

  /* USER CODE END USART1_Init 0 */

  /* USER CODE BEGIN USART1_Init 1 */

  /* USER CODE END USART1_Init 1 */
  huart1.Instance = USART1;
  huart1.Init.BaudRate = 115200;
  huart1.Init.WordLength = UART_WORDLENGTH_8B;
  huart1.Init.StopBits = UART_STOPBITS_1;
  huart1.Init.Parity = UART_PARITY_NONE;
  huart1.Init.Mode = UART_MODE_TX_RX;
  huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart1.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART1_Init 2 */
  
  /*清除USART1的中断*/
  USART1->SR; USART1->DR;
  __HAL_UART_CLEAR_FLAG(&huart1, UART_FLAG_RXNE);
  
  /*使能USART1的中断*/
  __HAL_UART_ENABLE_IT(&huart1, UART_IT_RXNE);
  __HAL_UART_ENABLE_IT(&huart1, UART_IT_IDLE);

  /* USER CODE END USART1_Init 2 */

}
/* USART2 init function */

void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */
  
  /*清除USART2的中断*/
  USART2->SR; USART2->DR;
  __HAL_UART_CLEAR_FLAG(&huart2, UART_FLAG_RXNE);
  
  /*使能USART2的中断*/
  __HAL_UART_ENABLE_IT(&huart2, UART_IT_RXNE);
  __HAL_UART_ENABLE_IT(&huart2, UART_IT_IDLE);

  /* USER CODE END USART2_Init 2 */

}
/* USART3 init function */

void MX_USART3_UART_Init(void)
{

  /* USER CODE BEGIN USART3_Init 0 */

  /* USER CODE END USART3_Init 0 */

  /* USER CODE BEGIN USART3_Init 1 */

  /* USER CODE END USART3_Init 1 */
  huart3.Instance = USART3;
  huart3.Init.BaudRate = 115200;
  huart3.Init.WordLength = UART_WORDLENGTH_8B;
  huart3.Init.StopBits = UART_STOPBITS_1;
  huart3.Init.Parity = UART_PARITY_NONE;
  huart3.Init.Mode = UART_MODE_TX_RX;
  huart3.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart3.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart3) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART3_Init 2 */
  
  /*清除USART3的中断*/
  USART3->SR; USART3->DR;
  __HAL_UART_CLEAR_FLAG(&huart3, UART_FLAG_RXNE);
  
  /*使能USART3的中断*/
  __HAL_UART_ENABLE_IT(&huart3, UART_IT_RXNE);
  __HAL_UART_ENABLE_IT(&huart3, UART_IT_IDLE);
  
  /* USER CODE END USART3_Init 2 */

}

void HAL_UART_MspInit(UART_HandleTypeDef* uartHandle)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};
  if(uartHandle->Instance==UART4)
  {
  /* USER CODE BEGIN UART4_MspInit 0 */

  /* USER CODE END UART4_MspInit 0 */
    /* UART4 clock enable */
    __HAL_RCC_UART4_CLK_ENABLE();

    __HAL_RCC_GPIOA_CLK_ENABLE();
    /**UART4 GPIO Configuration
    PA0-WKUP     ------> UART4_TX
    PA1     ------> UART4_RX
    */
    GPIO_InitStruct.Pin = GPIO_PIN_0|GPIO_PIN_1;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF8_UART4;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    /* UART4 interrupt Init */
    HAL_NVIC_SetPriority(UART4_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(UART4_IRQn);
  /* USER CODE BEGIN UART4_MspInit 1 */

  /* USER CODE END UART4_MspInit 1 */
  }
  else if(uartHandle->Instance==UART5)
  {
  /* USER CODE BEGIN UART5_MspInit 0 */

  /* USER CODE END UART5_MspInit 0 */
    /* UART5 clock enable */
    __HAL_RCC_UART5_CLK_ENABLE();

    __HAL_RCC_GPIOC_CLK_ENABLE();
    __HAL_RCC_GPIOD_CLK_ENABLE();
    /**UART5 GPIO Configuration
    PC12     ------> UART5_TX
    PD2     ------> UART5_RX
    */
    GPIO_InitStruct.Pin = GPIO_PIN_12;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF8_UART5;
    HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);

    GPIO_InitStruct.Pin = GPIO_PIN_2;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF8_UART5;
    HAL_GPIO_Init(GPIOD, &GPIO_InitStruct);

    /* UART5 interrupt Init */
    HAL_NVIC_SetPriority(UART5_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(UART5_IRQn);
  /* USER CODE BEGIN UART5_MspInit 1 */

  /* USER CODE END UART5_MspInit 1 */
  }
  else if(uartHandle->Instance==USART1)
  {
  /* USER CODE BEGIN USART1_MspInit 0 */

  /* USER CODE END USART1_MspInit 0 */
    /* USART1 clock enable */
    __HAL_RCC_USART1_CLK_ENABLE();

    __HAL_RCC_GPIOA_CLK_ENABLE();
    /**USART1 GPIO Configuration
    PA9     ------> USART1_TX
    PA10     ------> USART1_RX
    */
    GPIO_InitStruct.Pin = GPIO_PIN_9|GPIO_PIN_10;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF7_USART1;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    /* USART1 interrupt Init */
    HAL_NVIC_SetPriority(USART1_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(USART1_IRQn);
  /* USER CODE BEGIN USART1_MspInit 1 */

  /* USER CODE END USART1_MspInit 1 */
  }
  else if(uartHandle->Instance==USART2)
  {
  /* USER CODE BEGIN USART2_MspInit 0 */

  /* USER CODE END USART2_MspInit 0 */
    /* USART2 clock enable */
    __HAL_RCC_USART2_CLK_ENABLE();

    __HAL_RCC_GPIOA_CLK_ENABLE();
    /**USART2 GPIO Configuration
    PA2     ------> USART2_TX
    PA3     ------> USART2_RX
    */
    GPIO_InitStruct.Pin = GPIO_PIN_2|GPIO_PIN_3;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF7_USART2;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

    /* USART2 interrupt Init */
    HAL_NVIC_SetPriority(USART2_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(USART2_IRQn);
  /* USER CODE BEGIN USART2_MspInit 1 */

  /* USER CODE END USART2_MspInit 1 */
  }
  else if(uartHandle->Instance==USART3)
  {
  /* USER CODE BEGIN USART3_MspInit 0 */

  /* USER CODE END USART3_MspInit 0 */
    /* USART3 clock enable */
    __HAL_RCC_USART3_CLK_ENABLE();

    __HAL_RCC_GPIOB_CLK_ENABLE();
    /**USART3 GPIO Configuration
    PB10     ------> USART3_TX
    PB11     ------> USART3_RX
    */
    GPIO_InitStruct.Pin = GPIO_PIN_10|GPIO_PIN_11;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF7_USART3;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    /* USART3 interrupt Init */
    HAL_NVIC_SetPriority(USART3_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(USART3_IRQn);
  /* USER CODE BEGIN USART3_MspInit 1 */

  /* USER CODE END USART3_MspInit 1 */
  }
}

void HAL_UART_MspDeInit(UART_HandleTypeDef* uartHandle)
{

  if(uartHandle->Instance==UART4)
  {
  /* USER CODE BEGIN UART4_MspDeInit 0 */

  /* USER CODE END UART4_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_UART4_CLK_DISABLE();

    /**UART4 GPIO Configuration
    PA0-WKUP     ------> UART4_TX
    PA1     ------> UART4_RX
    */
    HAL_GPIO_DeInit(GPIOA, GPIO_PIN_0|GPIO_PIN_1);

    /* UART4 interrupt Deinit */
    HAL_NVIC_DisableIRQ(UART4_IRQn);
  /* USER CODE BEGIN UART4_MspDeInit 1 */

  /* USER CODE END UART4_MspDeInit 1 */
  }
  else if(uartHandle->Instance==UART5)
  {
  /* USER CODE BEGIN UART5_MspDeInit 0 */

  /* USER CODE END UART5_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_UART5_CLK_DISABLE();

    /**UART5 GPIO Configuration
    PC12     ------> UART5_TX
    PD2     ------> UART5_RX
    */
    HAL_GPIO_DeInit(GPIOC, GPIO_PIN_12);

    HAL_GPIO_DeInit(GPIOD, GPIO_PIN_2);

    /* UART5 interrupt Deinit */
    HAL_NVIC_DisableIRQ(UART5_IRQn);
  /* USER CODE BEGIN UART5_MspDeInit 1 */

  /* USER CODE END UART5_MspDeInit 1 */
  }
  else if(uartHandle->Instance==USART1)
  {
  /* USER CODE BEGIN USART1_MspDeInit 0 */

  /* USER CODE END USART1_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_USART1_CLK_DISABLE();

    /**USART1 GPIO Configuration
    PA9     ------> USART1_TX
    PA10     ------> USART1_RX
    */
    HAL_GPIO_DeInit(GPIOA, GPIO_PIN_9|GPIO_PIN_10);

    /* USART1 interrupt Deinit */
    HAL_NVIC_DisableIRQ(USART1_IRQn);
  /* USER CODE BEGIN USART1_MspDeInit 1 */

  /* USER CODE END USART1_MspDeInit 1 */
  }
  else if(uartHandle->Instance==USART2)
  {
  /* USER CODE BEGIN USART2_MspDeInit 0 */

  /* USER CODE END USART2_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_USART2_CLK_DISABLE();

    /**USART2 GPIO Configuration
    PA2     ------> USART2_TX
    PA3     ------> USART2_RX
    */
    HAL_GPIO_DeInit(GPIOA, GPIO_PIN_2|GPIO_PIN_3);

    /* USART2 interrupt Deinit */
    HAL_NVIC_DisableIRQ(USART2_IRQn);
  /* USER CODE BEGIN USART2_MspDeInit 1 */

  /* USER CODE END USART2_MspDeInit 1 */
  }
  else if(uartHandle->Instance==USART3)
  {
  /* USER CODE BEGIN USART3_MspDeInit 0 */

  /* USER CODE END USART3_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_USART3_CLK_DISABLE();

    /**USART3 GPIO Configuration
    PB10     ------> USART3_TX
    PB11     ------> USART3_RX
    */
    HAL_GPIO_DeInit(GPIOB, GPIO_PIN_10|GPIO_PIN_11);

    /* USART3 interrupt Deinit */
    HAL_NVIC_DisableIRQ(USART3_IRQn);
  /* USER CODE BEGIN USART3_MspDeInit 1 */

  /* USER CODE END USART3_MspDeInit 1 */
  }
}

/* USER CODE BEGIN 1 */

/********************************************************************/


/*Emm_V5发送数据函数*/
/**
  * @brief  USART发送多个字节
  * @param  __IO uint8_t *cmd, uint8_t len
  * @retval 无
  */
void usart_SendCmd(__IO uint8_t *cmd, uint8_t len, UART_HandleTypeDef* huart)
{
	__IO uint8_t i = 0;
	
	for(i=0; i < len; i++) { usart_SendByte(cmd[i], huart); }
}

/**
  * @brief  USART发送一个字节
  * @param  uint16_t data
  * @retval 无
  */
void usart_SendByte(uint16_t data, UART_HandleTypeDef* huart)
{
	__IO uint16_t t0 = 0;
	
	huart->Instance->DR = (data & (uint16_t)0x01FF);

	while(!(huart->Instance->SR & UART_FLAG_TXE))
	{
		++t0; if(t0 > 8000)	{	return; }
	}
}

/********************************************************************/

/**
  * @brief This function handles USART1 global interrupt.
  */
void USART1_IRQHandler(void)
{
  /* USER CODE BEGIN USART1_IRQn 0 */

  /* USER CODE END USART1_IRQn 0 */
//  HAL_UART_IRQHandler(&huart1);
  /* USER CODE BEGIN USART1_IRQn 1 */
	
	__IO uint16_t i = 0;
	
	/*串口接收中断*/
	if(__HAL_UART_GET_FLAG(&huart1, UART_FLAG_RXNE) != RESET)
	{
		//未完成一帧数据接收，数据进入缓冲队列
		fifo_enQueue_usart1((uint8_t)USART1->DR);

		//清除串口接收中断
		__HAL_UART_CLEAR_FLAG(&huart1, UART_FLAG_RXNE);
	}
	
	/*串口空闲中断*/
	else if(__HAL_UART_GET_FLAG(&huart1, UART_FLAG_IDLE) != RESET)
	{
		//先读SR再读DR，清除IDLE中断
		USART1->SR; USART1->DR;

		//提取一帧数据命令
		usart1_rxCount = fifo_queueLength_usart1(); for(i=0; i < usart1_rxCount; i++) { usart1_rxCmd[i] = fifo_deQueue_usart1(); }

		//一帧数据接收完成，位置帧标志位
		usart1_rxFrameFlag = true;
	}

  /* USER CODE END USART1_IRQn 1 */
}

/**
  * @brief This function handles USART2 global interrupt.
  */
void USART2_IRQHandler(void)
{
  /* USER CODE BEGIN USART2_IRQn 0 */

  /* USER CODE END USART2_IRQn 0 */
//  HAL_UART_IRQHandler(&huart2);
  /* USER CODE BEGIN USART2_IRQn 1 */
	
	__IO uint16_t i = 0;
	
	/*串口接收中断*/
	if(__HAL_UART_GET_FLAG(&huart2, UART_FLAG_RXNE) != RESET)
	{
		//未完成一帧数据接收，数据进入缓冲队列
		fifo_enQueue_usart2((uint8_t)USART2->DR);

		//清除串口接收中断
		__HAL_UART_CLEAR_FLAG(&huart2, UART_FLAG_RXNE);
	}
	
	/*串口空闲中断*/
	else if(__HAL_UART_GET_FLAG(&huart2, UART_FLAG_IDLE) != RESET)
	{
		//先读SR再读DR，清除IDLE中断
		USART2->SR; USART2->DR;

		//提取一帧数据命令
		usart2_rxCount = fifo_queueLength_usart2(); for(i=0; i < usart2_rxCount; i++) { usart2_rxCmd[i] = fifo_deQueue_usart2(); }

		//一帧数据接收完成，位置帧标志位
		usart2_rxFrameFlag = true;
	}

  /* USER CODE END USART2_IRQn 1 */
}

/**
  * @brief This function handles USART3 global interrupt.
  */
void USART3_IRQHandler(void)
{
  /* USER CODE BEGIN USART3_IRQn 0 */

  /* USER CODE END USART3_IRQn 0 */
//  HAL_UART_IRQHandler(&huart3);
  /* USER CODE BEGIN USART3_IRQn 1 */
	
	__IO uint16_t i = 0;
	
	/*串口接收中断*/
	if(__HAL_UART_GET_FLAG(&huart3, UART_FLAG_RXNE) != RESET)
	{
		//未完成一帧数据接收，数据进入缓冲队列
		fifo_enQueue_usart3((uint8_t)USART3->DR);

		//清除串口接收中断
		__HAL_UART_CLEAR_FLAG(&huart3, UART_FLAG_RXNE);
	}
	
	/*串口空闲中断*/
	else if(__HAL_UART_GET_FLAG(&huart3, UART_FLAG_IDLE) != RESET)
	{
		//先读SR再读DR，清除IDLE中断
		USART3->SR; USART3->DR;

		//提取一帧数据命令
		usart3_rxCount = fifo_queueLength_usart3(); for(i=0; i < usart3_rxCount; i++) { usart3_rxCmd[i] = fifo_deQueue_usart3(); }

		//一帧数据接收完成，位置帧标志位
		usart3_rxFrameFlag = true;
	}

  /* USER CODE END USART3_IRQn 1 */
}

/**
  * @brief This function handles UART4 global interrupt.
  */
void UART4_IRQHandler(void)
{
  /* USER CODE BEGIN UART4_IRQn 0 */

  /* USER CODE END UART4_IRQn 0 */
//  HAL_UART_IRQHandler(&huart4);
  /* USER CODE BEGIN UART4_IRQn 1 */
	
	__IO uint16_t i = 0;
	
	/*串口接收中断*/
	if(__HAL_UART_GET_FLAG(&huart4, UART_FLAG_RXNE) != RESET)
	{
		//未完成一帧数据接收，数据进入缓冲队列
		fifo_enQueue_uart4((uint8_t)UART4->DR);

		//清除串口接收中断
		__HAL_UART_CLEAR_FLAG(&huart4, UART_FLAG_RXNE);
	}
	
	/*串口空闲中断*/
	else if(__HAL_UART_GET_FLAG(&huart4, UART_FLAG_IDLE) != RESET)
	{
		//先读SR再读DR，清除IDLE中断
		UART4->SR; UART4->DR;

		//提取一帧数据命令
		uart4_rxCount = fifo_queueLength_uart4(); for(i=0; i < uart4_rxCount; i++) { uart4_rxCmd[i] = fifo_deQueue_uart4(); }

		//一帧数据接收完成，位置帧标志位
		uart4_rxFrameFlag = true;
	}

  /* USER CODE END UART4_IRQn 1 */
}

/**
  * @brief This function handles UART5 global interrupt.
  */
void UART5_IRQHandler(void)
{
  /* USER CODE BEGIN UART5_IRQn 0 */

  /* USER CODE END UART5_IRQn 0 */
//  HAL_UART_IRQHandler(&huart5);
  /* USER CODE BEGIN UART5_IRQn 1 */
	
	uint8_t data;
	uint8_t integer_x, decimal_x;
	uint8_t integer_y, decimal_y;
	
	if(__HAL_UART_GET_FLAG(&huart5, UART_FLAG_RXNE) != RESET)
	{
		data = UART5->DR;
		
		if(rx_bufferIndex == 0 && data == 0xAA)			//检查第一帧头
		{
			rx_openmv_buffer[rx_bufferIndex++] = data;	//保存第一帧头
		}
		else if(rx_bufferIndex == 1 && data == 0xBB)	//检查第二帧头
		{
			rx_openmv_buffer[rx_bufferIndex++] = data;	//保存第二帧头
		}
		else if(rx_bufferIndex == 10 && data == 0xFF)	//检查帧尾
		{
			rx_openmv_buffer[rx_bufferIndex++] = data;	//保存帧尾
			
			if(rx_bufferIndex == 11)		//接收完整数据包
			{
				if(rx_openmv_buffer[0] == 0xAA && rx_openmv_buffer[1] == 0xBB && rx_openmv_buffer[10] == 0xFF)	//再次检查帧头、帧尾
				{
					openmv_colourflag_plate = rx_openmv_buffer[2];		//保存颜色标志位——药板
					openmv_colourflag_bottle = rx_openmv_buffer[3];		//保存颜色标志位——药瓶
					openmv_statusflag = rx_openmv_buffer[4];			//保存状态标志位
					openmv_quadrantflag = rx_openmv_buffer[5];			//保存象限标志位
					
					/*uint8_t转化位float，保存坐标数据，传来的单位是mm，因此转换为cm*/
					integer_x = rx_openmv_buffer[6];
					decimal_x = rx_openmv_buffer[7];
					integer_y = rx_openmv_buffer[8];
					decimal_y = rx_openmv_buffer[9];
					
					openmv_x = (float)integer_x / 10.0f + (float)decimal_x / 1000.0f;
					openmv_y = (float)integer_y / 10.0f + (float)decimal_y / 1000.0f;
					
					
					if(openmv_quadrantflag == 1)
					{
						openmv_x = openmv_x;
						openmv_y = openmv_y;
					}
					else if(openmv_quadrantflag == 2)
					{
						openmv_x = -openmv_x;
						openmv_y = openmv_y;
					}
					else if(openmv_quadrantflag == 3)
					{
						openmv_x = -openmv_x;
						openmv_y = -openmv_y;
					}
					else if(openmv_quadrantflag == 4)
					{
						openmv_x = openmv_x;
						openmv_y = -openmv_y;
					}
				}
				
				rx_bufferIndex = 0;		//清空数据缓冲区，为下一条数据做准备
			}
		}
		else if(rx_bufferIndex < 10)		//保存数据
		{
			rx_openmv_buffer[rx_bufferIndex++] = data;
		}
		else		//错误清零操作
		{
			rx_bufferIndex = 0;
		}
		
		//清除串口接收中断
		__HAL_UART_CLEAR_FLAG(&huart5, UART_FLAG_RXNE);
	}

  /* USER CODE END UART5_IRQn 1 */
}


/* USER CODE END 1 */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
