#include "fifo.h"
/*fifo 先入先出函数（队列函数）*/

__IO FIFO_t rxFIFO_usart1 = {0};
__IO FIFO_t rxFIFO_usart2 = {0};
__IO FIFO_t rxFIFO_usart3 = {0};
__IO FIFO_t rxFIFO_uart4 = {0};

/**
	* @brief   初始化队列
	* @param   无
	* @retval  无
	*/
void initQueue_usart1(void)
{
	rxFIFO_usart1.ptrRead  = 0;
	rxFIFO_usart1.ptrWrite = 0;
}

/**
	* @brief   入队
	* @param   无
	* @retval  无
	*/
void fifo_enQueue_usart1(uint16_t data)
{
	rxFIFO_usart1.buffer[rxFIFO_usart1.ptrWrite] = data;
	
	++rxFIFO_usart1.ptrWrite;
	
	if(rxFIFO_usart1.ptrWrite >= FIFO_SIZE)
	{
		rxFIFO_usart1.ptrWrite = 0;
	}
}

/**
	* @brief   出队
	* @param   无
	* @retval  无
	*/
uint16_t fifo_deQueue_usart1(void)
{
	uint16_t element = 0;

	element = rxFIFO_usart1.buffer[rxFIFO_usart1.ptrRead];

	++rxFIFO_usart1.ptrRead;

	if(rxFIFO_usart1.ptrRead >= FIFO_SIZE)
	{
		rxFIFO_usart1.ptrRead = 0;
	}

	return element;
}

/**
	* @brief   判断空队列
	* @param   无
	* @retval  无
	*/
bool fifo_isEmpty_usart1(void)
{
	if(rxFIFO_usart1.ptrRead == rxFIFO_usart1.ptrWrite)
	{
		return true;
	}

	return false;
}

/**
	* @brief   计算队列长度
	* @param   无
	* @retval  无
	*/
uint16_t fifo_queueLength_usart1(void)
{
	if(rxFIFO_usart1.ptrRead <= rxFIFO_usart1.ptrWrite)
	{
		return (rxFIFO_usart1.ptrWrite - rxFIFO_usart1.ptrRead);
	}
	else
	{
		return (FIFO_SIZE - rxFIFO_usart1.ptrRead + rxFIFO_usart1.ptrWrite);
	}
}

/***************************************************************************************/

/**
	* @brief   初始化队列
	* @param   无
	* @retval  无
	*/
void initQueue_usart2(void)
{
	rxFIFO_usart2.ptrRead  = 0;
	rxFIFO_usart2.ptrWrite = 0;
}

/**
	* @brief   入队
	* @param   无
	* @retval  无
	*/
void fifo_enQueue_usart2(uint16_t data)
{
	rxFIFO_usart2.buffer[rxFIFO_usart2.ptrWrite] = data;
	
	++rxFIFO_usart2.ptrWrite;
	
	if(rxFIFO_usart2.ptrWrite >= FIFO_SIZE)
	{
		rxFIFO_usart2.ptrWrite = 0;
	}
}

/**
	* @brief   出队
	* @param   无
	* @retval  无
	*/
uint16_t fifo_deQueue_usart2(void)
{
	uint16_t element = 0;

	element = rxFIFO_usart2.buffer[rxFIFO_usart2.ptrRead];

	++rxFIFO_usart2.ptrRead;

	if(rxFIFO_usart2.ptrRead >= FIFO_SIZE)
	{
		rxFIFO_usart2.ptrRead = 0;
	}

	return element;
}

/**
	* @brief   判断空队列
	* @param   无
	* @retval  无
	*/
bool fifo_isEmpty_usart2(void)
{
	if(rxFIFO_usart2.ptrRead == rxFIFO_usart2.ptrWrite)
	{
		return true;
	}

	return false;
}

/**
	* @brief   计算队列长度
	* @param   无
	* @retval  无
	*/
uint16_t fifo_queueLength_usart2(void)
{
	if(rxFIFO_usart2.ptrRead <= rxFIFO_usart2.ptrWrite)
	{
		return (rxFIFO_usart2.ptrWrite - rxFIFO_usart2.ptrRead);
	}
	else
	{
		return (FIFO_SIZE - rxFIFO_usart2.ptrRead + rxFIFO_usart2.ptrWrite);
	}
}

/***************************************************************************************/

/**
	* @brief   初始化队列
	* @param   无
	* @retval  无
	*/
void initQueue_usart3(void)
{
	rxFIFO_usart3.ptrRead  = 0;
	rxFIFO_usart3.ptrWrite = 0;
}

/**
	* @brief   入队
	* @param   无
	* @retval  无
	*/
void fifo_enQueue_usart3(uint16_t data)
{
	rxFIFO_usart3.buffer[rxFIFO_usart3.ptrWrite] = data;
	
	++rxFIFO_usart3.ptrWrite;
	
	if(rxFIFO_usart3.ptrWrite >= FIFO_SIZE)
	{
		rxFIFO_usart3.ptrWrite = 0;
	}
}

/**
	* @brief   出队
	* @param   无
	* @retval  无
	*/
uint16_t fifo_deQueue_usart3(void)
{
	uint16_t element = 0;

	element = rxFIFO_usart3.buffer[rxFIFO_usart3.ptrRead];

	++rxFIFO_usart3.ptrRead;

	if(rxFIFO_usart3.ptrRead >= FIFO_SIZE)
	{
		rxFIFO_usart3.ptrRead = 0;
	}

	return element;
}

/**
	* @brief   判断空队列
	* @param   无
	* @retval  无
	*/
bool fifo_isEmpty_usart3(void)
{
	if(rxFIFO_usart3.ptrRead == rxFIFO_usart3.ptrWrite)
	{
		return true;
	}

	return false;
}

/**
	* @brief   计算队列长度
	* @param   无
	* @retval  无
	*/
uint16_t fifo_queueLength_usart3(void)
{
	if(rxFIFO_usart3.ptrRead <= rxFIFO_usart3.ptrWrite)
	{
		return (rxFIFO_usart3.ptrWrite - rxFIFO_usart3.ptrRead);
	}
	else
	{
		return (FIFO_SIZE - rxFIFO_usart3.ptrRead + rxFIFO_usart3.ptrWrite);
	}
}


/***************************************************************************************/

/**
	* @brief   初始化队列
	* @param   无
	* @retval  无
	*/
void initQueue_uart4(void)
{
	rxFIFO_uart4.ptrRead  = 0;
	rxFIFO_uart4.ptrWrite = 0;
}

/**
	* @brief   入队
	* @param   无
	* @retval  无
	*/
void fifo_enQueue_uart4(uint16_t data)
{
	rxFIFO_uart4.buffer[rxFIFO_uart4.ptrWrite] = data;
	
	++rxFIFO_uart4.ptrWrite;
	
	if(rxFIFO_uart4.ptrWrite >= FIFO_SIZE)
	{
		rxFIFO_uart4.ptrWrite = 0;
	}
}

/**
	* @brief   出队
	* @param   无
	* @retval  无
	*/
uint16_t fifo_deQueue_uart4(void)
{
	uint16_t element = 0;

	element = rxFIFO_uart4.buffer[rxFIFO_uart4.ptrRead];

	++rxFIFO_uart4.ptrRead;

	if(rxFIFO_uart4.ptrRead >= FIFO_SIZE)
	{
		rxFIFO_uart4.ptrRead = 0;
	}

	return element;
}

/**
	* @brief   判断空队列
	* @param   无
	* @retval  无
	*/
bool fifo_isEmpty_uart4(void)
{
	if(rxFIFO_uart4.ptrRead == rxFIFO_uart4.ptrWrite)
	{
		return true;
	}

	return false;
}

/**
	* @brief   计算队列长度
	* @param   无
	* @retval  无
	*/
uint16_t fifo_queueLength_uart4(void)
{
	if(rxFIFO_uart4.ptrRead <= rxFIFO_uart4.ptrWrite)
	{
		return (rxFIFO_uart4.ptrWrite - rxFIFO_uart4.ptrRead);
	}
	else
	{
		return (FIFO_SIZE - rxFIFO_uart4.ptrRead + rxFIFO_uart4.ptrWrite);
	}
}


