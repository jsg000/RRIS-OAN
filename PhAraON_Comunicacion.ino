#include <AccelStepper.h>
#include <ArduinoRS485.h> //Esta libreria se encuentra por defecto en https://wokwi.com

String coor, altu, azim;   //maximum expected length 
int paso1 ; //distance in mm from the computer
int paso2; //delay between two steps, received from the computer
int sep;
// direction Digital 9 (CCW), pulses Digital 8 (CLK)
AccelStepper stepper1(1, 8, 9);
AccelStepper stepper2(1, 6, 7); 
void setup() {
  Serial.begin(9600);
  while (!Serial);
  RS485.begin(9600);
  // enable reception, can be disabled with: RS485.noReceive();
  RS485.receive();
  stepper1.setMaxSpeed(2000); //SPEED = Steps / second
  stepper1.setAcceleration(1000); //ACCELERATION = Steps /(second)^2
  stepper2.setMaxSpeed(2000); //SPEED = Steps / second
  stepper2.setAcceleration(1000); //ACCELERATION = Steps /(second)^2
}
void datos(){
if (RS485.available()>0) {
    coor= RS485.readString();
    sep=coor.indexOf(' ');
    altu=coor.substring(0,sep);
    azim=coor.substring(sep+1);
    paso1=altu.toInt();
    paso2=azim.toInt();
    stepper1.setSpeed(400); //set speed 
  stepper1.move(paso1); 
  stepper2.setSpeed(400); 
  stepper2.move(paso2);  
    
   }
  
}
void loop(){
  datos();
  if(paso1!=0){
  stepper1.run();//set speed 
  }
  if(paso2!=0){  
  stepper2.run(); 
  }
  
  }
