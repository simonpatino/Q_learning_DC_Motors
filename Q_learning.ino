#include <AFMotor.h>

AF_DCMotor motor(4);

int encoder_one;

int encoder_two;

void setup() {
  motor.setSpeed(0);
  motor.run(RELEASE);
  
  Serial.begin(9600);
}

void loop() {

  
  if ( Serial.available() > 0) {
    
    String data_fc = Serial.readStringUntil("\n");
    
    }

  set_velocity(200);
  forward();
}

void forward() {
  motor.run(FORWARD);
}
void backward() {
  motor.run(BACKWARD);
}
void v_zero() {
  motor.run(RELEASE); 
}

int set_velocity(int vel)   //from [0,255]
{   
  motor.setSpeed(vel);
}
