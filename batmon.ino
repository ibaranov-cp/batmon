/* 
 * rosserial ADC Example
 * 
 * This is a poor man's Oscilloscope.  It does not have the sampling 
 * rate or accuracy of a commerical scope, but it is great to get
 * an analog value into ROS in a pinch.
 */
#define USE_USBCON 1
#include <ros.h>
#include <batmon/bat_data.h>

ros::NodeHandle_<ArduinoHardware, 10, 10, 200, 200> nh;

batmon::bat_data data_msg;
ros::Publisher p("BATMON", &data_msg);

#include <Wire.h>
#include "ina219.h"

INA219 monitor1;
INA219 monitor2;
INA219 monitor3;
INA219 monitor4;

void setup()
{ 
  pinMode(13, OUTPUT);
  nh.initNode();

  nh.advertise(p);
  
  //INA219 coms
  monitor1.begin(64);
  monitor2.begin(65);
  monitor3.begin(66);
  monitor4.begin(67);
  monitor1.configure(1, 0, 3, 3, 7); //0-32V, 40mV range
  monitor2.configure(1, 0, 3, 3, 7); //0-32V, 40mV range,
  monitor3.configure(1, 0, 3, 3, 7); //0-32V, 40mV range,
  monitor4.configure(1, 0, 3, 3, 7); //0-32V, 40mV range,
        
  
  // test shunt = 115mm of 22AWG solid copper = 0.3 Ohms
  monitor1.calibrate(0.02, 0.04, 19, 10);
  monitor2.calibrate(0.02, 0.04, 19, 10);
  monitor3.calibrate(0.02, 0.04, 19, 10);
  monitor4.calibrate(0.02, 0.04, 19, 10);
}

//We average the analog reading to elminate some of the noise
int averageAnalog(int pin){
  int v=0;
  for(int i=0; i<4; i++) v+= analogRead(pin);
  return v/4;
}

long adc_timer;

void loop()
{
    
  p.publish(&data_msg);

  nh.spinOnce();
}

