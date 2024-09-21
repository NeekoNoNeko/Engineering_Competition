/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
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
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

#include "delay.h"
#include "Emm_V5.h"
#include "Servo.h"
#include "key.h"
#include "motor.h"
#include "position.h"
#include "OLED.h"
#include "pump.h"

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

void OLED_Showcolor(uint8_t colorflag1, uint8_t colorflag2);

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

uint8_t KeyNum;

//int8_t Speed;		//šƿ�ǵ���ٶȣ�����������ת����Χ -100~100
__IO uint16_t Emm_speed = 1000;		//42������������ٶȣ���λ�������X,Y,Z������
__IO uint8_t Emm_Z_acc = 60;		//Z�ᶨλ������ٶ�

/*openmv*/
__IO float openmv_x, openmv_y;			//openmv��������
__IO uint8_t openmv_colourflag_plate;	//openmv��ɫ��־λ��1 red; 2 green; 3 blue����ʾ��oled��
__IO uint8_t openmv_colourflag_bottle;	//openmv��ɫ��־λ��1 red; 2 green; 3 blue����ʾ��oled��
__IO uint8_t openmv_statusflag;			//openmv״̬��־λ��1 ҩ��; 2 ҩƿ; 3 šƿ��; #δʹ��#4 ���ж���ֻ�����жϴ��
__IO uint8_t openmv_quadrantflag;		//openmv���ޱ�־λ��1 ��һ����; 2 �ڶ�����; 3 ��������; 4 ��������		
uint8_t send_statusdata[5] = {0xA1, 0xA2, 0, 0, 0xFE};		//���͸�openmv��״̬���ݰ�
		//λ2�����ظ�openmv��״̬��־λ��0 Ĭ��λ; 1 ��λ׼��ץȡ; 2 ���ץȡ; 3 ��ʼʶ��ɫ��; #δʹ��#4 ���������źŸ����ص�Ƭ��
		//λ3��ģʽλ��ҩ�塢ҩƿ or ƿ�ǣ���0 Ĭ��λ; 1 ҩ��; 2 ҩƿ; 3 ƿ��

/*�����ϸ���Ʒλ�ã�ҩ�塢ҩƿ������*/
__IO float plate_x = 24.681, plate_y = 5.872;		//ҩ��λ�ã�������ϢΪҩ�����ĵ�λ��
__IO float bottle_x = 28.096, bottle_y = 23.652;	//ҩƿλ��
__IO float cap_x = 15.365, cap_y = 24.288;			//ƿ��λ��
__IO float tray_x = 11.292, tray_y = 12.495;		//����λ�ã�������ϢΪ�������ĵ�λ��

float err_x = -5.8, err_y = -0.45;					//�Ӿ�ģ�������õ�ƫ����
float plate_err_x = -4.0, plate_err_y = -2.0;		//ҩ��������ҩ��׵�ƫ����
/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */
	
	__IO uint8_t i = 0;
//	__IO uint8_t j = 0;
	__IO uint8_t times_plate = 0;
	__IO uint8_t times_bottle = 0;

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_UART4_Init();
  MX_UART5_Init();
  MX_USART1_UART_Init();
  MX_USART2_UART_Init();
  MX_USART3_UART_Init();
  MX_TIM3_Init();
  MX_TIM4_Init();
  /* USER CODE BEGIN 2 */
  
  OLED_Init();
  delay_init(168);
  
  /*��ʱ�ȴ�3s��ʼ�����*/
  delay_ms(3000);
  
  XYZ_Return_Origin(2);		//��ʼ������

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
	  
	/*����ֵ*/
	KeyNum = key_num();
	  
	i++;
	OLED_ShowNum(0, 0, i, 3, OLED_8X16);
	OLED_Update();
	
/*****************************************************************************************************/
	if(KeyNum == 1 || openmv_statusflag == 1)
	{	
		send_statusdata[3] = 1;		//ģʽΪҩ��
		HAL_UART_Transmit(&huart5, send_statusdata, 5, 50);
		
		/*******************************************************************************/
		OLED_ShowString(0, 16, "plate :", OLED_6X8);
		OLED_ShowNum(42, 16, KeyNum, 2, OLED_6X8);
		OLED_Update();

		Tray_position();	//��λ����λ��
		
		/*���͵�λ��־���Ӿ������Ӿ�����ʶ��*/
		send_statusdata[2] = 1;		//��λ�Ӿ�ʶ��
		HAL_UART_Transmit(&huart5, send_statusdata, 5, 50);
		delay_ms(5000);		//Ԥ���Ӿ����ʱ��
		
		/*******************************************************************************/
		/*��ʾ�Ӿ����������ҩ�������������*/
		OLED_ShowFloatNum(0, 24, openmv_x, 3, 3, OLED_6X8);
		OLED_ShowFloatNum(0, 32, openmv_y, 3, 3, OLED_6X8);
		OLED_Update();
		
		OLED_Showcolor(openmv_colourflag_plate, openmv_colourflag_bottle);		//��ץȡҩ����ɫ
		
		/*******************************************************************************/
		
		/*����ץȡ��ɱ�־���Ӿ�������ֹͣʶ��*/
		send_statusdata[2] = 2;		//�����ץȡ�Ӿ��ɹر�
		HAL_UART_Transmit(&huart5, send_statusdata, 5, 50);
		
		/*��ʼ��λҩ��*/
		delay_ms(1000);
		X_Emm_V5_position(tray_x + openmv_x + err_x, Emm_speed);
		Y_Emm_V5_position(tray_y + openmv_y + err_y, Emm_speed);
		while(x_arrive_check() == false || y_arrive_check() == false);

		Z_Emm_V5_position(1.55, Emm_speed);
		while(z_arrive_check() == false);
		
		/*******************************************************************************/
		pump_control(1);
		valve_control(0);
		
		delay_ms(1000);		//Ԥ�����������ȶ�ʱ��
		Z_Emm_V5_position(12, Emm_speed);
		while(z_arrive_check() == false);
		
		/*��λҩ��λ��*/
		X_Emm_V5_position(plate_x + plate_err_x + err_x, Emm_speed);
		Y_Emm_V5_position(plate_y + plate_err_y + err_y, Emm_speed);
		while(x_arrive_check() == false || y_arrive_check() == false);
		
		Z_Emm_V5_position(2.4, Emm_speed);
		while(z_arrive_check() == false);
		
		/*******************************************************************************/
		Plate_HolePitch_position();		//ҩ���ƫ���������

//		j ++;
//		if(j == 1)
//		{
//			plate_y = plate_y + 0.4f;
//		}
//		else if(j == 2)
//		{
//			plate_y = plate_y + 0.4f;
//		}
//		else if(j == 3)
//		{
//			plate_y = plate_y - 0.8f;
//			plate_x = plate_x + 0.4f;
//		}
//		else if(j == 4)
//		{
//			plate_y = plate_y + 0.4f;
//		}
//		else if(j == 5)
//		{
//			plate_y = plate_y + 0.4f;
//		}
		
		/*******************************************************************************/
		pump_control(0);
		valve_control(1);
		delay_ms(500);
		valve_control(0);		//��ŷ����ܳ�ʱ��򿪣�������ܻᷢ������

		/*******************************************************************************/
		times_plate++;			//ץȡҩ�赽ҩ�����������ץȡҩ�赽ҩ��ĸ���
		OLED_ShowNum(66, 16, times_plate, 3, OLED_6X8);
		OLED_Update();
		
		if(times_plate == 6)
		{
			send_statusdata[3] = 2;		//ģʽת��Ϊҩƿ
			HAL_UART_Transmit(&huart5, send_statusdata, 5, 50);
		}
		
//		openmv_statusflag = 0;		//�������
	}
	
/*****************************************************************************************************/
	if(KeyNum == 2 || openmv_statusflag == 2)
	{
		send_statusdata[3] = 2;		//ģʽת��Ϊҩƿ
		HAL_UART_Transmit(&huart5, send_statusdata, 5, 50);
		
		/*******************************************************************************/
		OLED_ShowString(0, 16, "bottle:", OLED_6X8);
		OLED_ShowNum(42, 16, KeyNum, 2, OLED_6X8);
		OLED_Update();

		Tray_position();	//��λ����λ��
		
		/*���͵�λ��־���Ӿ������Ӿ�����ʶ��*/
		send_statusdata[2] = 1;		//��λ�Ӿ�ʶ��
		HAL_UART_Transmit(&huart5, send_statusdata, 5, 50);
		delay_ms(5000);		//Ԥ���Ӿ����ʱ��
		
		/*******************************************************************************/
		/*��ʾ�Ӿ����������ҩ�������������*/
		OLED_ShowFloatNum(0, 24, openmv_x, 3, 3, OLED_6X8);
		OLED_ShowFloatNum(0, 32, openmv_y, 3, 3, OLED_6X8);
		OLED_Update();
		
		OLED_Showcolor(openmv_colourflag_plate, openmv_colourflag_bottle);		//��ץȡҩ����ɫ
		
		/*******************************************************************************/
		/*����ץȡ��ɱ�־���Ӿ�������ֹͣʶ��*/
		send_statusdata[2] = 2;		//�����ץȡ�Ӿ��ɹر�
		HAL_UART_Transmit(&huart5, send_statusdata, 5, 50);
		
		/*��ʼ��λҩ��*/
		X_Emm_V5_position(tray_x + openmv_x + err_x, Emm_speed);
		Y_Emm_V5_position(tray_y + openmv_y + err_y, Emm_speed);
		while(x_arrive_check() == false || y_arrive_check() == false);

		Z_Emm_V5_position(1.55, Emm_speed);
		while(z_arrive_check() == false);
		
		/*******************************************************************************/
		pump_control(1);
		valve_control(0);
		
		delay_ms(1000);		//Ԥ�����������ȶ�ʱ��
		Z_Emm_V5_position(12, Emm_speed);
		while(z_arrive_check() == false);
		
		/*��λҩƿλ��*/
		X_Emm_V5_position(bottle_x + err_x, Emm_speed);
		Y_Emm_V5_position(bottle_y + err_y, Emm_speed);
		while(x_arrive_check() == false || y_arrive_check() == false);
		
		Z_Emm_V5_position(7.55, Emm_speed);
		while(z_arrive_check() == false);
		
		/*******************************************************************************/
		pump_control(0);
		valve_control(1);
		delay_ms(500);
		valve_control(0);	//��ŷ����ܳ�ʱ��򿪣�������ܻᷢ������
		
		/*******************************************************************************/
		times_bottle++;		//ץȡҩ�赽ҩƿ����������ץȡҩ�赽ҩƿ�Ĵ���
		OLED_ShowNum(90, 16, times_bottle, 3, OLED_6X8);
		OLED_Update();
		
		if(times_bottle == 6)
		{
			KeyNum = 3;
		}
		
//		openmv_statusflag = 0;
	}
	
/*****************************************************************************************************/
	if(KeyNum == 3 || openmv_statusflag == 3)
	{
		OLED_ShowString(0, 16, "cap   :", OLED_6X8);
		OLED_ShowNum(42, 16, KeyNum, 2, OLED_6X8);
		OLED_Update();
		
		/*******************************************************************************/
		Z_Emm_V5_position(12, Emm_speed);
		while(z_arrive_check() == false);
		
		/*��λƿ��λ��*/
		X_Emm_V5_position(cap_x + err_x, Emm_speed);
		Y_Emm_V5_position(cap_y + err_y, Emm_speed);
		while(x_arrive_check() == false || y_arrive_check() == false);
		
		Z_Emm_V5_position(1.3, Emm_speed);
		while(z_arrive_check() == false);
		
		/*******************************************************************************/
		pump_control(1);
		valve_control(0);
		
		/*******************************************************************************/
		delay_ms(1000);		//Ԥ��������ƿ���ȶ�ʱ��
		Z_Emm_V5_position(12, Emm_speed);
		while(z_arrive_check() == false);
		
		/*��λҩƿλ��*/
		X_Emm_V5_position(bottle_x + err_x, Emm_speed);
		Y_Emm_V5_position(bottle_y + err_y, Emm_speed);
		while(x_arrive_check() == false || y_arrive_check() == false);
		
		Z_Emm_V5_position(9, Emm_speed);
		while(z_arrive_check() == false);
		
		/*******************************************************************************/
		pump_control(0);
		valve_control(1);
		
		delay_ms(1000);
		Clamp_Emm_V5_position(10.35, 100, 30);		//λ�ã��ٶȣ����ٶ�
		
		Z_Emm_V5_position(12, Emm_speed);
		while(z_arrive_check() == false);
		
		valve_control(0);	//��ŷ����ܳ�ʱ��򿪣�������ܻᷢ������
		
		/*******************************************************************************/
		/*����ɳ���ֱ�ӻ���*/
		OLED_ShowString(0, 16, "retrun:", OLED_6X8);
		OLED_ShowNum(42, 16, KeyNum, 2, OLED_6X8);
		OLED_Update();
		
		XYZ_Return_Origin(2);
		
		/*******************************************************************************/
//		Motor_SetSpeed(100);
//		delay_ms(1000);
		delay_ms(3000);
		Motor_SetSpeed(-100);
		delay_ms(3000);
		Motor_SetSpeed(0);
	}
	
/*****************************************************************************************************/
	if(KeyNum == 4)
	{
		OLED_ShowString(0, 16, "card  :", OLED_6X8);
		OLED_ShowNum(42, 16, KeyNum, 2, OLED_6X8);
		OLED_Update();
		
//		Z_Emm_V5_position(12, 500);
//		while(z_arrive_check() == false);
//		
//		XYZ_Return_Origin(2);
		
		/*���ͼ��ɫ����־λ���Ӿ�����������ɫ��ʶ��*/
		send_statusdata[2] = 3;		//ʶ��ɫ����ɫ
		HAL_UART_Transmit(&huart5, send_statusdata, 5, 50);
		
		send_statusdata[2] = 0;
		
		OLED_Showcolor(openmv_colourflag_plate, openmv_colourflag_bottle);		//��ץȡҩ����ɫ
	}
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);
  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 8;
  RCC_OscInitStruct.PLL.PLLN = 168;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV2;
  RCC_OscInitStruct.PLL.PLLQ = 4;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV4;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_5) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

void OLED_Showcolor(uint8_t colorflag1, uint8_t colorflag2)
{
	if(colorflag1 == 1)
	{
		OLED_ShowString(0, 48, "plate:Red  ", OLED_6X8);
		OLED_Update();
	}
	else if(colorflag1 == 2)
	{
		OLED_ShowString(0, 48, "plate:Green", OLED_6X8);
		OLED_Update();
	}
	else if(colorflag1 == 3)
	{
		OLED_ShowString(0, 48, "plate:Bule ", OLED_6X8);
		OLED_Update();
	}
	
	if(colorflag2 == 1)
	{
		OLED_ShowString(0, 56, "bottle:Red  ", OLED_6X8);
		OLED_Update();
	}
	else if(colorflag2 == 2)
	{
		OLED_ShowString(0, 56, "bottle:Green", OLED_6X8);
		OLED_Update();
	}
	else if(colorflag2 == 3)
	{
		OLED_ShowString(0, 56, "bottle:Bule ", OLED_6X8);
		OLED_Update();
	}
}

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
