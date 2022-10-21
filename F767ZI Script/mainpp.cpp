#include <mainpp.h>
#include <ros.h>
#include <std_msgs/Float64.h>
#include <sensor_msgs/Joy.h>

extern TIM_HandleTypeDef htim1;

ros::NodeHandle nh;

std_msgs::Float64 val;
ros::Publisher duty("duty_cycle", &val);

void joy_cb(const sensor_msgs::Joy& vel_msg);

ros::Subscriber<sensor_msgs::Joy> joy_sub("joy", &joy_cb);

void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart){
  nh.getHardware()->flush();
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart){
  nh.getHardware()->reset_rbuf();
}

void setup(void)
{
  nh.initNode();
  nh.advertise(duty);
  nh.subscribe(joy_sub);

  HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_1);
}

void loop(void)
{
  duty.publish(&val);

  nh.spinOnce();

  HAL_Delay(10);
}

void joy_cb(const sensor_msgs::Joy& vel_msg)
{
	float joy_val = vel_msg.axes[1];
	float duty_c = joy_val * 100;
	
    	__HAL_TIM_SET_COMPARE(&htim1,TIM_CHANNEL_1, duty_c*400);

  	val.data = duty_c;
	duty.publish(&val);
}
