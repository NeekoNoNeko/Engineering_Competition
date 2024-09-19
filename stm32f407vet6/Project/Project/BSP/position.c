#include "position.h"

/*X轴数据*/
//float last_x;
//uint32_t x_pulse;
//uint32_t last_x_pulse;
//uint8_t dir_x;

/*Y轴数据*/
//float last_y;
//uint32_t y_pulse;
//uint32_t last_y_pulse;
//uint8_t dir_y;

/*Z轴数据*/
//float last_z;
//uint32_t z_pulse;
//uint32_t last_z_pulse;
//uint8_t dir_z;

/*上述变量改为以下结构体*/
struct CSYS
{
	float last_coord;			//上次坐标
	uint32_t pulse;				//脉冲
	uint32_t last_pulse;		//上次脉冲
	uint8_t dir;				//方向变量，范围 0~1 ；0为反转，1为正转
}X, Y, Z, Clamp;

__IO uint8_t j = 0;
/*托盘上各物品位置，药板、药瓶、托盘*/
extern __IO float plate_x, plate_y;			//药板位置
extern __IO float tray_x, tray_y;			//托盘位置

extern __IO uint16_t Emm_speed;		//42步进电机运行速度
extern __IO uint8_t Emm_Z_acc;		//Z轴电机加速度

/*在整个定位程序中，z轴的优先级应该要是最高的，即在z轴没有到达指定位置前，x轴和y轴不能有动作*/
__IO bool z_arriveflag = false;			//z轴到位标志位
__IO bool x_arriveflag = false;			//x轴到位标志位
__IO bool y_arriveflag = false;			//y轴到位标志位


/*****************************************************************************************************/

/**
  * @brief  X轴定位
  * @param  x，X轴定位坐标，范围 0~49，单位cm
  * @param	velocity，电机速度
  * @retval 无
  */
void X_Emm_V5_position(float x, uint16_t velocity)
{
//	x_arriveflag = false;
	
	X.pulse = round((double)(x + Offset_X) / Step * Step_Pulse);
	X.last_pulse = round((double)(X.last_coord + Offset_X) / Step * Step_Pulse);
	
	/*方向判断*/
	if(x < X.last_coord)	//新点比旧点小，初始旧点变量参数都为0
	{
		X.dir = 0;		//反转
		X.pulse = X.last_pulse - X.pulse;
	}
	else if(x > X.last_coord)
	{
		X.dir = 1;		//正转
		X.pulse = X.pulse - X.last_pulse;
	}
	else if(x == X.last_coord)
	{
		X.dir = 1;
		X.pulse = 0;
	}
	
	Emm_V5_Pos_Control(1, X.dir, velocity, 0, X.pulse, 0, 0, 1);		//1号电机（X轴电机）
	/*等待返回命令，命令数据缓存在数组rxCmd上，长度为rxCount*/
	while(usart1_rxFrameFlag == false);
	usart1_rxFrameFlag = false;
	
	X.last_coord = x;
	
	/*到位判断*/
//	while(1)
//	{
//		if(usart1_rxCmd[0] == 0x01 && usart1_rxCmd[3] == 0x6B && usart1_rxCount == 4)
//		{
//			if(usart1_rxCmd[1] == 0xFD && usart1_rxCmd[2] == 0x9F)
//			{
//				OLED_ShowString(0, 40, "arr_x", OLED_6X8);
//				OLED_Update();
//				break;
//			}
//		}
//	}
}

/**
  * @brief  Y轴定位
  * @param  y，Y轴定位坐标，范围 0~26，单位cm
  * @param	velocity，电机速度
  * @retval 无
  */
void Y_Emm_V5_position(float y, uint16_t velocity)
{
//	y_arriveflag = false;
	
	Y.pulse = round((double)(y + Offset_Y) / Step * Step_Pulse);
	Y.last_pulse = round((double)(Y.last_coord + Offset_Y) / Step * Step_Pulse);
	
	/*方向判断*/
	if(y < Y.last_coord)	//新点比旧点小，初始旧点变量参数都为0
	{
		Y.dir = 0;		//反转
		Y.pulse = Y.last_pulse - Y.pulse;
	}
	else if(y > Y.last_coord)
	{
		Y.dir = 1;		//正转
		Y.pulse = Y.pulse - Y.last_pulse;
	}
	else if(y == Y.last_coord)
	{
		Y.dir = 1;
		Y.pulse = 0;
	}
	
	Emm_V5_Pos_Control(1, Y.dir, velocity, 0, Y.pulse, 0, 0, 2);		//2号电机（Y轴电机）
	/*等待返回命令，命令数据缓存在数组rxCmd上，长度为rxCount*/
	while(usart2_rxFrameFlag == false);
	usart2_rxFrameFlag = false;
	
	Y.last_coord = y;
	
	/*到位判断*/
//	while(1)
//	{
//		if(usart2_rxCmd[0] == 0x01 && usart2_rxCmd[3] == 0x6B && usart2_rxCount == 4)
//		{
//			if(usart2_rxCmd[1] == 0xFD && usart2_rxCmd[2] == 0x9F)
//			{
//				OLED_ShowString(36, 40, "arr_y", OLED_6X8);
//				OLED_Update();
//				break;
//			}
//		}
//	}
}

/**
  * @brief  Z轴定位
  * @param  z，Z轴定位坐标，范围 0~18，单位cm
  * @param	velocity，电机速度
  * @retval 无
  */
void Z_Emm_V5_position(float z, uint16_t velocity)
{
//	z_arriveflag = false;
	
	Z.pulse = round((double)(z + Offset_Z) / Step * Step_Pulse);
	Z.last_pulse = round((double)(Z.last_coord + Offset_Z) / Step * Step_Pulse);
	
	/*方向判断*/
	if(z < Z.last_coord)	//新点比旧点小，初始旧点变量参数都为0
	{
		Z.dir = 1;		//反转
		Z.pulse = Z.last_pulse - Z.pulse;
	}
	else if(z > Z.last_coord)
	{
		Z.dir = 0;		//正转
		Z.pulse = Z.pulse - Z.last_pulse;
	}
	else if(z == Z.last_coord)
	{
		Z.dir = 0;
		Z.pulse = 0;
	}
	
	Emm_V5_Pos_Control(1, Z.dir, velocity, Emm_Z_acc, Z.pulse, 0, 0, 4);		//4号电机（Z轴电机）
	/*等待返回命令，命令数据缓存在数组rxCmd上，长度为rxCount*/
	while(uart4_rxFrameFlag == false);
	uart4_rxFrameFlag = false;
	
	Z.last_coord = z;
	
	/*到位判断*/
//	while(1)
//	{
//		if(uart4_rxCmd[0] == 0x01 && uart4_rxCmd[3] == 0x6B && uart4_rxCount == 4)
//		{
//			if(uart4_rxCmd[1] == 0xFD && uart4_rxCmd[2] == 0x9F)
//			{
//				OLED_ShowString(72, 40, "arr_z", OLED_6X8);
//				OLED_Update();
//				break;
//			}
//		}
//	}
}

/**
  * @brief  药瓶推挤夹持电机距离函数
  * @param  clamp，加持移动距离，范围 0~10.3，单位cm
  * @param	velocity，电机速度
  * @param	accelerated_speed，电机加速度
  * @retval 无
  */
void Clamp_Emm_V5_position(float clamp, uint16_t velocity, uint8_t accelerated_speed)
{
	Clamp.pulse = round((double)(clamp + Offset_Clamp) / Step * Step_Pulse);
	Clamp.last_pulse = round((double)(Clamp.last_coord + Offset_Clamp) / Step * Step_Pulse);
	
	/*方向判断*/
	if(clamp < Clamp.last_coord)	//新点比旧点小，初始旧点变量参数都为0
	{
		Clamp.dir = 1;		//反转
		Clamp.pulse = Clamp.last_pulse - Clamp.pulse;
	}
	else if(clamp > Clamp.last_coord)
	{
		Clamp.dir = 0;		//正转
		Clamp.pulse = Clamp.pulse - Clamp.last_pulse;
	}
	else if(clamp == Clamp.last_coord)
	{
		Clamp.dir = 1;
		Clamp.pulse = 0;
	}
	
	Emm_V5_Pos_Control(1, Clamp.dir, velocity, accelerated_speed, Clamp.pulse, 0, 0, 3);		//3号电机（药瓶推挤夹持电机）
	/*等待返回命令，命令数据缓存在数组rxCmd上，长度为rxCount*/
	while(usart3_rxFrameFlag == false);
	usart3_rxFrameFlag = false;
	
	Clamp.last_coord = clamp;
}


/*****************************************************************************************************/

/**
  * @brief  XYZ轴回零函数
  * @param  Mode，回零模式
  *			0 单圈就近回零；1 单圈方向回零；2 多圈无限位碰撞回零；3 多圈有限位开关回零
  * @retval 无
  */
void XYZ_Return_Origin(uint8_t Mode)
{
//	/*z轴回零相关参数*/
//	float z_up_cm = 10.0;	//z轴回零上升高度，单位cm
//	uint32_t z_Orogin_up;	//z轴回零上升脉冲数
//	
//	z_Orogin_up = round((double)z_up_cm / Step * Step_Pulse);
//	
//	/*z轴回零上升高度，防止撞击托盘上的物品，至少上升10cm*/
//	Emm_V5_Pos_Control(1, 0, 100, 0, z_Orogin_up, 0, 0, 3);
//	/*等待返回命令，命令数据缓存在数组rxCmd上，长度为rxCount*/
//	while(rxFrameFlag == false);
//	rxFrameFlag = false;
	
	/*X轴回零*/
	Emm_V5_Origin_Trigger_Return(1, Mode, 0, 1);
	/*等待返回命令，命令数据缓存在数组rxCmd上，长度为rxCount*/
	while(usart1_rxFrameFlag == false);
	usart1_rxFrameFlag = false;
	
	/*Y轴回零*/
	Emm_V5_Origin_Trigger_Return(1, Mode, 0, 2);
	/*等待返回命令，命令数据缓存在数组rxCmd上，长度为rxCount*/
	while(usart2_rxFrameFlag == false);
	usart2_rxFrameFlag = false;
	
	/*Z轴回零*/
	Emm_V5_Origin_Trigger_Return(1, Mode, 0, 4);
	/*等待返回命令，命令数据缓存在数组rxCmd上，长度为rxCount*/
	while(uart4_rxFrameFlag == false);
	uart4_rxFrameFlag = false;
}


/*****************************************************************************************************/

/**
  * @brief  药盘孔位置定位与移动
  * @param  无
  * @retval 无
  */
void Plate_HolePitch_position(void)
{
	j ++;
	switch(j)
	{
		case 1:		//第2孔
		{
			plate_x += Plate_HolePitch;
		}break;
		case 2:		//第3孔
		{
			plate_x += Plate_HolePitch;
		}break;
		case 3:		//第4孔
		{
			plate_x = plate_x - Plate_HolePitch * 2;
			plate_y += Plate_HolePitch;
		}break;
		case 4:		//第5孔
		{
			plate_x += Plate_HolePitch;
		}break;
		case 5:		//第6孔
		{
			plate_x += Plate_HolePitch;
		}break;
	}
}

/**
  * @brief  托盘定位
  * @param  无
  * @retval 无
  */
void Tray_position(void)
{
	Z_Emm_V5_position(12, Emm_speed);
	while(z_arrive_check() == false);
	
	X_Emm_V5_position(tray_x, Emm_speed);
	Y_Emm_V5_position(tray_y, Emm_speed);
	while(x_arrive_check() == false || y_arrive_check() == false);
}


/*****************************************************************************************************/

/**
  * @brief  z轴到位检测
  * @param  无
  * @retval 无
  */
bool z_arrive_check(void)
{
	z_arriveflag = false;
	
	if(uart4_rxCmd[0] == 0x01 && uart4_rxCmd[3] == 0x6B && uart4_rxCount == 4)
	{
		if(uart4_rxCmd[1] == 0xFD && uart4_rxCmd[2] == 0x9F)
		{
			z_arriveflag = true;
		}
	}
	return z_arriveflag;
}

/**
  * @brief  x轴到位检测
  * @param  无
  * @retval 无
  */
bool x_arrive_check(void)
{
	x_arriveflag = false;
	
	if(usart1_rxCmd[0] == 0x01 && usart1_rxCmd[3] == 0x6B && usart1_rxCount == 4)
	{
		if(usart1_rxCmd[1] == 0xFD && usart1_rxCmd[2] == 0x9F)
		{
			x_arriveflag = true;
		}
	}
	return x_arriveflag;
}

bool y_arrive_check(void)
{
	y_arriveflag = false;
	
	if(usart2_rxCmd[0] == 0x01 && usart2_rxCmd[3] == 0x6B && usart2_rxCount == 4)
	{
		if(usart2_rxCmd[1] == 0xFD && usart2_rxCmd[2] == 0x9F)
		{
			y_arriveflag = true;
		}
	}
	return y_arriveflag;
}

