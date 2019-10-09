// uses cycle-all-valves as base code and arduino digital read serial tutorial
#include "Pam.h"

// Create global PAM (pneumatic artificial muscle) controller
Pam Pam(0x77); // argument is i2c address

// Other globals
long t = 0;  // loop counter
float p[4];  // array of pressures (one for each channel)
float threshold; // for pressure reading

// set button variable to make or break pin - also connects to gnd thru resistor
int button = 10;
// other (power) pin should go to a terminal of the LED

void setup() {

  Serial.begin(9600);

  // Init PAM
  Pam.begin();

  // Set valve pins for each PAM channel
  Pam.setupChannel(0, 2, 3); // arguments: ch, a_pin, b_pin
  Pam.setupChannel(1, 4, 5);
  Pam.setupChannel(2, 6, 7);
  Pam.setupChannel(3, 8, 9);

  Serial.begin(9600);
  
  // set button pin as input
  pinMode(button, INPUT_PULLUP);
}

void loop() {

  // Possible valve commands (1 == high pressure, -1 == exhaust, 0 == closed)
  int u[3] = {1, -1, 0};
  // read input
  int buttonState = digitalRead(button);
//
//  // loop through all channels and commands
// for (int ch=0; ch<4; ch++) { //A
  if (buttonState == HIGH){

//look up threshold control in library
    
    Pam.setValves(0,u[0]);// input air
    delay(2000); //for 2 seconds
    
    threshold = Pam.getPressure(0);
    if (threshold > 20){ //change to 10 for less pressure
      Pam.setValves(0,u[2]); //hold the pressure
      delay(5000); //for 5 seconds
    }
  }
  else{
    Pam.setValves(0,u[1]);
  }

//  p[ch] = Pam.getPressure(ch); //A
  p[0] = Pam.getPressure(0); // sample each channels pressure
  p[1] = Pam.getPressure(1);
  delay(100); // keep this setting for 1 sec after button is pressed
//  } //A

  Serial.print("Loop ");
  Serial.println(t++);
  Serial.print("Button State ");
  Serial.println(buttonState);
  Serial.print("p0 = ");
  Serial.print(p[0],2);
  Serial.print("\tp1 = ");
  Serial.print(p[1],2);
  Serial.println();
}
