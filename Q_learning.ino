#include <AFMotor.h>
#define ENCA_ONE A0
#define ENCA_TWO 2
#include <util/atomic.h>
#include <math.h>

AF_DCMotor motor(4);

volatile int posi = 0;
volatile float velocity = 0;
volatile long prevT = 0;
volatile int pos_i = 0;



void setup() {

  //
  motor.setSpeed(0);
  motor.run(FORWARD);
  //
  pinMode(INPUT, ENCA_ONE);
  pinMode( INPUT, ENCA_TWO);
  attachInterrupt(digitalPinToInterrupt(ENCA_TWO), readEncoder, RISING);
  //
  Serial.begin(9600);
}

void loop() {

int pos = 0;
float velocity2; 

  ATOMIC_BLOCK(ATOMIC_RESTORESTATE){
    pos = pos_i;
    
    velocity2 = velocity ;
  }
int vel_to_send;
  vel_to_send=  round((velocity2*60)/(12*64)); 
Serial.println(vel_to_send);

delay(200);
  if (Serial.available() > 0) {
    
    String data_fc = Serial.readStringUntil("\r");
    data_fc.trim();

    //Serial.println(data_fc.toInt());


    //set_velocity(data_fc.toInt()) ;

    motor.setSpeed(data_fc.toInt());
    
    //if(data_fc =="1"){

    //forward();
    //}

    //if(data_fc =="0"){
    //v_zero();  
    //  } 

    //if(data_fc =="-1"){

    //backward();
    //}

   }




  
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

void readEncoder()
{
  
  int b = digitalRead(ENCA_ONE);
  int increment = 0;
 
  if (b > 0) {
    increment = 1;
  }
  else {
    increment = -1;
  }
  pos_i = pos_i + increment; 
  long currT = micros();
  float deltaT = ((float)(currT - prevT)) / 1.0e6 ; 
  velocity = increment / deltaT;
  prevT = currT;

}
