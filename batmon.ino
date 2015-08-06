
#define USE_USBCON 1
#include <ros.h>
#include <batmon/bat_data.h>
#include <std_msgs/UInt8.h>

ros::NodeHandle_<ArduinoHardware, 10, 10, 100, 100> nh; //10,10,200,200

#include <Wire.h>
#include "ina219.h"

INA219 monitor1;
INA219 monitor2;
INA219 monitor3;
INA219 monitor4;

//Pin Defines
#define B3_C 5  // PC6(PB0)
#define B3_D 8  // PB4
#define B4_C 9  // PB5
#define B4_D 11 // PB7
#define B2_C 12 // PD6
#define B2_D 6  // PD7
#define B1_C 4  // PD4
#define B1_D 7  // PE6

//voltage,current,power,temp feedback from each of 4 batteries
batmon::bat_data data_msg;
ros::Publisher p("BATMON", &data_msg);

//callbacks for enabling/disabling batteries
void B1_cb( const std_msgs::UInt8& cmd_msg) {
  monitor1.reset();
  monitor1.configure(1, 1, 3, 3, 7); //0-32V, 80mV range
  monitor1.calibrate(0.02, 0.08, 19, 10);
  if (cmd_msg.data == 1) { //charge
    digitalWrite(B1_D, LOW);
    delay(100);
    digitalWrite(B1_C, HIGH);
  }
  else if (cmd_msg.data == 2) { //discharge
    digitalWrite(B1_C, LOW);
    delay(100);
    digitalWrite(B1_D, HIGH);
  }
  else {
    digitalWrite(B1_C, LOW);
    digitalWrite(B1_D, LOW);
  }
}
void B2_cb( const std_msgs::UInt8& cmd_msg) {
  monitor2.reset();
  monitor2.configure(1, 1, 3, 3, 7); //0-32V, 80mV range
  monitor2.calibrate(0.02, 0.08, 19, 10);
  if (cmd_msg.data == 1) { //charge
    digitalWrite(B2_D, LOW);
    delay(100);
    digitalWrite(B2_C, HIGH);
  }
  else if (cmd_msg.data == 2) { //discharge
    digitalWrite(B2_C, LOW);
    delay(100);
    digitalWrite(B2_D, HIGH);    
  }
  else {
    digitalWrite(B2_C, LOW);
    digitalWrite(B2_D, LOW);
  }
}
void B3_cb( const std_msgs::UInt8& cmd_msg) {
  monitor3.reset();
  monitor3.configure(1, 1, 3, 3, 7); //0-32V, 80mV range
  monitor3.calibrate(0.02, 0.08, 19, 10);
  if (cmd_msg.data == 1) { //charge
    digitalWrite(B3_D, LOW);
    delay(100);
    digitalWrite(B3_C, HIGH);    
  }
  else if (cmd_msg.data == 2) { //discharge
    digitalWrite(B3_C, LOW);
    delay(100);
    digitalWrite(B3_D, HIGH);    
  }
  else {
    digitalWrite(B3_C, LOW);
    digitalWrite(B3_D, LOW);
  }
}
void B4_cb( const std_msgs::UInt8& cmd_msg) {
  monitor4.reset();
  monitor4.configure(1, 1, 3, 3, 7); //0-32V, 80mV range
  monitor4.calibrate(0.02, 0.08, 19, 10);
  if (cmd_msg.data == 1) { //charge
    digitalWrite(B4_D, LOW);
    delay(100);
    digitalWrite(B4_C, HIGH);    
  }
  else if (cmd_msg.data == 2) { //discharge
    digitalWrite(B4_C, LOW);
    delay(100);
    digitalWrite(B4_D, HIGH);    
  }
  else {
    digitalWrite(B4_C, LOW);
    digitalWrite(B4_D, LOW);
  }
}


ros::Subscriber<std_msgs::UInt8> sub1("B1", B1_cb);
ros::Subscriber<std_msgs::UInt8> sub2("B2", B2_cb);
ros::Subscriber<std_msgs::UInt8> sub3("B3", B3_cb);
ros::Subscriber<std_msgs::UInt8> sub4("B4", B4_cb);

void setup()
{
  pinMode(B1_C , OUTPUT);
  pinMode(B1_D , OUTPUT);
  pinMode(B2_C , OUTPUT);
  pinMode(B2_D , OUTPUT);
  pinMode(B3_C , OUTPUT);
  pinMode(B3_D , OUTPUT);
  pinMode(B4_C , OUTPUT);
  pinMode(B4_D , OUTPUT);
  
  digitalWrite(B1_C, LOW);
  digitalWrite(B1_D, LOW);
  digitalWrite(B2_C, LOW);
  digitalWrite(B2_D, LOW);
  digitalWrite(B3_C, LOW);
  digitalWrite(B3_D, LOW);
  digitalWrite(B4_C, LOW);
  digitalWrite(B4_D, LOW);


  nh.initNode();

  nh.advertise(p);
  nh.subscribe(sub1);
  nh.subscribe(sub2);
  nh.subscribe(sub3);
  nh.subscribe(sub4);

  //INA219 coms
  monitor1.begin(72);
  monitor2.begin(76);
  monitor3.begin(64);
  monitor4.begin(68);
  monitor1.configure(1, 2, 3, 3, 7); //0-32V, 160mV range
  monitor2.configure(1, 2, 3, 3, 7); //0-32V, 160mV range,
  monitor3.configure(1, 2, 3, 3, 7); //0-32V, 160mV range,
  monitor4.configure(1, 2, 3, 3, 7); //0-32V, 160mV range,


  monitor1.calibrate(0.02, 0.12, 26, 5);
  monitor2.calibrate(0.02, 0.12, 26, 5);
  monitor3.calibrate(0.02, 0.12, 26, 5);
  monitor4.calibrate(0.02, 0.12, 26, 5);
}

//We average the analog reading to elminate some of the noise
int averageAnalog(int pin) {
  int v = 0;
  for (int i = 0; i < 4; i++) v += analogRead(pin);
  return v / 4;
}

long adc_timer;

void loop()
{

  // readings in mV, mA, mW and degrees C.
  data_msg.Bat1_Volt  = abs(monitor1.busVoltage()*1000.0);
  data_msg.Bat1_Curr  = abs(monitor1.shuntCurrent() * 1000.0);
  data_msg.Bat1_Power = abs(monitor1.busPower() * 1000.0);
  data_msg.Bat1_Temp  = 0;
  data_msg.Bat2_Volt  = abs(monitor2.busVoltage()*1000.0);
  data_msg.Bat2_Curr  = abs(monitor2.shuntCurrent() * 1000.0);
  data_msg.Bat2_Power = abs(monitor2.busPower() * 1000.0);
  data_msg.Bat2_Temp  = 0;
  data_msg.Bat3_Volt  = abs((monitor3.busVoltage()*1000.0));
  if (data_msg.Bat3_Volt > 4000) { data_msg.Bat3_Volt = (data_msg.Bat3_Volt*(-0.001) + 32.525)*1000;} //fix for offset voltage
  data_msg.Bat3_Curr  = abs(monitor3.shuntCurrent() * 1000.0);
  if (data_msg.Bat3_Curr > 1000) { data_msg.Bat3_Curr += 1000;} //fix for offset current
  data_msg.Bat3_Power = abs(monitor3.busPower() * 1000.0);
  data_msg.Bat3_Temp  = 0;
  data_msg.Bat4_Volt  = abs((monitor4.busVoltage()*1000.0));
  if (data_msg.Bat4_Volt > 4000) { data_msg.Bat4_Volt = (data_msg.Bat4_Volt*(-0.001) + 32.525)*1000;} //fix for offset voltage
  data_msg.Bat4_Curr  = abs(monitor4.shuntCurrent() * 1000.0);
  if (data_msg.Bat4_Curr > 1000) { data_msg.Bat4_Curr += 1000;} //fix for offset current
  data_msg.Bat4_Power = abs(monitor4.busPower() * 1000.0);
  data_msg.Bat4_Temp  = 0;

  p.publish(&data_msg);

  nh.spinOnce();
  
  delay(200);
}

