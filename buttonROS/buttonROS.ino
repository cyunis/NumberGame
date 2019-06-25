// uses cycle-all-valves as base code and arduino digital read serial tutorial
#include "Pam.h"
#include <ros.h>
#include <std_msgs/Bool.h>

// Create global PAM (pneumatic artificial muscle) controller
Pam Pam(0x77); // argument is i2c address

ros::NodeHandle nh;

std_msgs::Bool pushed_msg;
ros::Publisher pub_button("pushed", &pushed_msg);

// Other globals
long t = 0;  // loop counter
float p[4];  // array of pressures (one for each channel)
float threshold; // for pressure reading
const int button_pin = 10;
const int led_pin = 13;

bool last_reading;
long last_debounce_time=0;
long debounce_delay=50;
bool published = true;

void setup()
{

  
  nh.initNode();
  nh.advertise(pub_button);

    // Init PAM
  Pam.begin();
  
  //initialize an LED output pin 
  //and a input pin for our push button
  pinMode(led_pin, OUTPUT);
  pinMode(button_pin, INPUT);
  
  //Enable the pullup resistor on the button
  digitalWrite(button_pin, HIGH);
  
  //The button is a normally button
  last_reading = digitalRead(button_pin);
 
}

void loop()
{
  
  bool reading = digitalRead(button_pin);
  
  if (last_reading!= reading){
      last_debounce_time = millis();
      published = false;
  }
  
  //if the button value has not changed for the debounce delay, we know its stable
  if ( !published && (millis() - last_debounce_time)  > debounce_delay) {
    digitalWrite(led_pin, reading);
    pushed_msg.data = reading;
    pub_button.publish(&pushed_msg);
    published = true;
  }

  last_reading = reading;
  
  nh.spinOnce();
}



//// add the ROS libraries and string, float, bool message types
//#include <ros.h>
////#include <std_msgs/String.h>
//#include <std_msgs/Bool.h>
////#include <std_msgs/Float32.h>
//
//// rosserial objects are globally declared
//ros::NodeHandle nh; //instantiate node handle
//
//std_msgs::Bool pushed_msg;
////std_msgs::String str_msg;
//ros::Publisher pub_button("pushed", &pushed_msg);
////ros::Publisher chatter("chatter", &str_msg);
//

//

//
//// set button variable to make or break pin - also connects to gnd thru resistor
//int button = 10; // other (power) pin should go to a terminal of the LED
//bool last_reading;
//long last_debounce_time=0;
//long debounce_delay=50;
//bool published = true;
//
////from blink example - function for subscriber
////void messageCb( const std_msgs::String& toggle_msg){
////  digitalWrite(13, HIGH-digitalRead(13));   // blink the led
////  reference toggle_msg because its no longer empty (ex = pin 13)
////}
////
////ros::Subscriber<std_msgs::Empty> sub("toggle_led", &messageCb );
//
//
//void setup() {
//
//  nh.initNode();
//  nh.advertise(pub_button);
//  
////  Serial.begin(9600);
//

//
//  // Set valve pins for each PAM channel
//  Pam.setupChannel(0, 2, 3); // arguments: ch, a_pin, b_pin
//  Pam.setupChannel(1, 4, 5);
//  Pam.setupChannel(2, 6, 7);
//  Pam.setupChannel(3, 8, 9);
// 
//  // set button pin as input
//  pinMode(button, INPUT_PULLUP);
//
//  last_reading = digitalRead(button);
//}
//
//
//void loop() {
//
//  bool reading = digitalRead(button);
//  
//  if (last_reading!= reading){
//      last_debounce_time = millis();
//      published = false;
//  }
//  
//  //if the button value has not changed for the debounce delay, we know its stable
//  if ( !published && (millis() - last_debounce_time)  > debounce_delay) {
//    pushed_msg.data = reading;
//    pub_button.publish(&pushed_msg);
//    published = true;
//  }
//
//  last_reading = reading;
//  
//  // Possible valve commands (1 == high pressure, -1 == exhaust, 0 == closed)
//  int u[3] = {1, -1, 0};
//  // read input
//  int buttonState = digitalRead(button);
////
////  // loop through all channels and commands
//// for (int ch=0; ch<4; ch++) { //A
//  if (buttonState == HIGH){
//
////look up threshold control in library
//    
//    Pam.setValves(0,u[0]);// input air
//    delay(20); //for 2 seconds
//    
//    threshold = Pam.getPressure(0);
//    if (threshold > 20){ //change to 10 for less pressure
//      Pam.setValves(0,u[2]); //hold the pressure
//      delay(50); //for 5 seconds
//    }
//  }
//  else{
//    Pam.setValves(0,u[1]);
//  }
//
//////  p[ch] = Pam.getPressure(ch); //A
////  p[0] = Pam.getPressure(0); // sample each channels pressure
////  p[1] = Pam.getPressure(1);
////  delay(100); // keep this setting for 1 sec after button is pressed
//////  } //A
////
////  Serial.print("Loop ");
////  Serial.println(t++);
////  Serial.print("Button State ");
////  Serial.println(buttonState);
////  Serial.print("p0 = ");
////  Serial.print(p[0],2);
////  Serial.print("\tp1 = ");
////  Serial.print(p[1],2);
////  Serial.println();
//
//  nh.spinOnce();
//}
