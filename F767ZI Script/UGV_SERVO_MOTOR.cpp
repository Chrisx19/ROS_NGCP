#include <mainpp.h>
#include <ros.h>
#include <geometry_msgs/Twist.h>

extern TIM_HandleTypeDef htim1;
extern TIM_HandleTypeDef htim2;

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

  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_2);
  HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);

}

void loop(void)
{
  nh.spinOnce();

  HAL_Delay(1);								//rate of 10hz
}

void ugv_vel_cb(const geometry_msgs::Twist& ugv_vel_msg)	//callback function from subscribe
{

	int drive_duty_cycle = ugv_vel_msg.linear.x;//val: -100 <-> 100
	int servo = ugv_vel_msg.angular.z;			//val: -50 <-> 50

	htim2.Instance -> CCR1 = 75 + servo;

	if (drive_duty_cycle >= 0)					//Forward
	{
		__HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_1, drive_duty_cycle*400);
		__HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_2, 0);
	}
	else										//Backward
	{
		__HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_1, 0);
		__HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_2, (drive_duty_cycle*-1) *400);
	}


}
