#include <mainpp.h>
#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/Int16.h>

extern TIM_HandleTypeDef htim3;
extern TIM_HandleTypeDef htim4;

extern UART_HandleTypeDef huart1;
extern UART_HandleTypeDef huart3;
extern DMA_HandleTypeDef hdma_usart3_rx;
extern DMA_HandleTypeDef hdma_usart3_tx;


ros::NodeHandle nh;

void ugv_vel_cb(const geometry_msgs::Twist& ugv_vel_msg);

ros::Subscriber<geometry_msgs::Twist> ugv_vel_sub("cmd_vel_ugv", &ugv_vel_cb);	//subscribing a topic from rpi's topic

void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart){
  nh.getHardware()->flush();
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart){
  nh.getHardware()->reset_rbuf();
}

void setup(void)
{
  nh.initNode();
  nh.subscribe(ugv_vel_sub);

	HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
	HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_2);
	HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_3);
	HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_4);

	HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_1);
	HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_2);
	HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_3);
	HAL_TIM_PWM_Start(&htim4, TIM_CHANNEL_4);
}

void loop(void)
{
  nh.spinOnce();

  HAL_Delay(10);								//rate of 10hz
}

void ugv_vel_cb(const geometry_msgs::Twist& ugv_vel_msg)	//callback function from subscribe
{

	int drive_duty_cycle = ugv_vel_msg.linear.x;//val: -100 <-> 100

	if (drive_duty_cycle > 0)					//Forward
	{
		__HAL_TIM_SET_COMPARE(&htim3,TIM_CHANNEL_1, drive_duty_cycle*400);
		__HAL_TIM_SET_COMPARE(&htim3,TIM_CHANNEL_2, 0);

		__HAL_TIM_SET_COMPARE(&htim3,TIM_CHANNEL_3, drive_duty_cycle*400);
		__HAL_TIM_SET_COMPARE(&htim3,TIM_CHANNEL_4, 0);

		__HAL_TIM_SET_COMPARE(&htim4,TIM_CHANNEL_1, drive_duty_cycle*400);
		__HAL_TIM_SET_COMPARE(&htim4,TIM_CHANNEL_2, 0);

		__HAL_TIM_SET_COMPARE(&htim4,TIM_CHANNEL_3, drive_duty_cycle*400);
		__HAL_TIM_SET_COMPARE(&htim4,TIM_CHANNEL_4, 0);
	}
	else										//Backward
	{
		__HAL_TIM_SET_COMPARE(&htim3,TIM_CHANNEL_1, 0);
		__HAL_TIM_SET_COMPARE(&htim3,TIM_CHANNEL_2, (drive_duty_cycle) *400);

		__HAL_TIM_SET_COMPARE(&htim3,TIM_CHANNEL_3, 0);
		__HAL_TIM_SET_COMPARE(&htim3,TIM_CHANNEL_4, (drive_duty_cycle) *400);

		__HAL_TIM_SET_COMPARE(&htim4,TIM_CHANNEL_1, 0);
		__HAL_TIM_SET_COMPARE(&htim4,TIM_CHANNEL_2, (drive_duty_cycle) *400);

		__HAL_TIM_SET_COMPARE(&htim4,TIM_CHANNEL_3, 0);
		__HAL_TIM_SET_COMPARE(&htim4,TIM_CHANNEL_4, (drive_duty_cycle) *400);
	}
}
