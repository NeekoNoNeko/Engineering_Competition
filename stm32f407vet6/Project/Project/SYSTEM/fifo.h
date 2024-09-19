#ifndef __FIFO_H__
#define __FIFO_H__

#include "stm32f4xx_hal.h"
#include "stdbool.h"


#define 	FIFO_SIZE   128
typedef struct {
	uint16_t buffer[FIFO_SIZE];
	__IO uint8_t ptrWrite;
	__IO uint8_t ptrRead;
}FIFO_t;

extern __IO FIFO_t rxFIFO_usart1;
extern __IO FIFO_t rxFIFO_usart2;
extern __IO FIFO_t rxFIFO_usart3;
extern __IO FIFO_t rxFIFO_uart4;

void initQueue_usart1(void);
void fifo_enQueue_usart1(uint16_t data);
uint16_t fifo_deQueue_usart1(void);
bool fifo_isEmpty_usart1(void);
uint16_t fifo_queueLength_usart1(void);

void initQueue_usart2(void);
void fifo_enQueue_usart2(uint16_t data);
uint16_t fifo_deQueue_usart2(void);
bool fifo_isEmpty_usart2(void);
uint16_t fifo_queueLength_usart2(void);

void initQueue_usart3(void);
void fifo_enQueue_usart3(uint16_t data);
uint16_t fifo_deQueue_usart3(void);
bool fifo_isEmpty_usart3(void);
uint16_t fifo_queueLength_usart3(void);

void initQueue_uart4(void);
void fifo_enQueue_uart4(uint16_t data);
uint16_t fifo_deQueue_uart4(void);
bool fifo_isEmpty_uart4(void);
uint16_t fifo_queueLength_uart4(void);

#endif
