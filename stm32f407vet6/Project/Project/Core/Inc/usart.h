/**
  ******************************************************************************
  * @file    usart.h
  * @brief   This file contains all the function prototypes for
  *          the usart.c file
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
/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __USART_H__
#define __USART_H__

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* USER CODE BEGIN Includes */
	
#include "sys.h"
#include "fifo.h"

/* USER CODE END Includes */

extern UART_HandleTypeDef huart4;
extern UART_HandleTypeDef huart5;
extern UART_HandleTypeDef huart1;
extern UART_HandleTypeDef huart2;
extern UART_HandleTypeDef huart3;

/* USER CODE BEGIN Private defines */

/*Emm_V5队列缓冲区参数*/
/*usart1*/
extern __IO bool usart1_rxFrameFlag;
extern __IO uint8_t usart1_rxCmd[FIFO_SIZE];
extern __IO uint8_t usart1_rxCount;
/*usart2*/
extern __IO bool usart2_rxFrameFlag;
extern __IO uint8_t usart2_rxCmd[FIFO_SIZE];
extern __IO uint8_t usart2_rxCount;
/*usart3*/
extern __IO bool usart3_rxFrameFlag;
extern __IO uint8_t usart3_rxCmd[FIFO_SIZE];
extern __IO uint8_t usart3_rxCount;
/*uart4*/
extern __IO bool uart4_rxFrameFlag;
extern __IO uint8_t uart4_rxCmd[FIFO_SIZE];
extern __IO uint8_t uart4_rxCount;


/* USER CODE END Private defines */

void MX_UART4_Init(void);
void MX_UART5_Init(void);
void MX_USART1_UART_Init(void);
void MX_USART2_UART_Init(void);
void MX_USART3_UART_Init(void);

/* USER CODE BEGIN Prototypes */

/*Emm_V5发送数据函数*/
void usart_SendCmd(__IO uint8_t *cmd, uint8_t len, UART_HandleTypeDef* huart);
void usart_SendByte(uint16_t data, UART_HandleTypeDef* huart);

/* USER CODE END Prototypes */

#ifdef __cplusplus
}
#endif

#endif /* __USART_H__ */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
