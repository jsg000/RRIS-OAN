#include <AccelStepper.h>
#define AM A1
#define PM A3
#define pin_X    4
#define pinX     5
#define pin_Y    7
#define pinY      2
#define y_dirL 6   // Define el Pin de STEP para Motor de eje X
#define y_dirR  9   // Define el Pin de DIR  para Motor de eje X
#define x_paso 10   // Define el Pin de STEP para Motor de eje Y
#define x_dire 12
bool ejecutada = false;
bool X;
bool X_;
bool Y;
bool Y_;
int t=1600;
AccelStepper stepper(1,x_paso,x_dire);

void setup() {
Serial.begin(9600);    //Iniciando puerto serial

pinMode(y_dirR,OUTPUT); // ustaw Pin9 jako PUL
pinMode(y_dirL,OUTPUT);
pinMode(x_paso,OUTPUT); // ustaw Pin9 jako PUL
pinMode(x_dire,OUTPUT); // ustaw Pin8 jako DIR

pinMode(pin_X,INPUT_PULLUP);
pinMode(pinX,INPUT_PULLUP);
pinMode(pin_Y,INPUT_PULLUP);
pinMode(pinY,INPUT_PULLUP);

pinMode(AM, INPUT_PULLUP);
pinMode(PM, INPUT_PULLUP);
stepper.setMaxSpeed(350);//12000
stepper.moveTo(-210);//0.7 grados
stepper.setSpeed(350);
stepper.setAcceleration(1); 
}
int movimiento=42000;//70 grados
int velocidad= 350;
void loop() {
if(digitalRead(AM)==LOW)
  {
  if(ejecutada == false) {  
  analogWrite(y_dirL, 255);
  delay(800);
  analogWrite(y_dirL,0); 
  stepper.move(210);//2.5 grados 
  stepper.run();
  ejecutada = true;
  }
  
  stepper.moveTo(movimiento);//0.7 grados orig:420,450 en vel
  stepper.setSpeed(velocidad);

  if(stepper.distanceToGo()==0) 
  {
    stepper.move(-(stepper.currentPosition()));
    stepper.setSpeed(velocidad);
  }
  while (stepper.distanceToGo()!=0)
  {
  stepper.runSpeedToPosition();
  }
   
} 
else{
  X = digitalRead(pinX);
  X_ = digitalRead(pin_X);  
  Y = digitalRead(pinY);
  Y_ = digitalRead(pin_Y);

  if(X==LOW){
    stepper.setSpeed(velocidad);  // Velocidad hacia la derecha
    stepper.runSpeed();
    }
  else if(X_==LOW){
    stepper.setSpeed(-1*(velocidad));  // Velocidad hacia la derecha
    stepper.runSpeed();
    }
  else{
    stepper.setSpeed(0);
    stepper.runSpeed();
    
    }

  if(Y==LOW){
  
    analogWrite(y_dirR, 0);
    analogWrite(y_dirL, 255);
    }

  else if(Y_==LOW){
  
    analogWrite(y_dirR, 255);
    analogWrite(y_dirL, 0);   
    }

  else{
  
  analogWrite(y_dirR, 0);
  analogWrite(y_dirL, 0);
  }
}
if (digitalRead(PM)==LOW)
{
 if(ejecutada == false) {  
  analogWrite(y_dirR, 255);
  delay(800);
  analogWrite(y_dirR, 0); 
  stepper.move(-210);
  stepper.run();//a un lado 0.35 grados 
  ejecutada = true;
  }
  
//stepper.setSpeed(600); 
  stepper.moveTo(movimiento);//0.7 grados
  stepper.setSpeed(velocidad);

  if(stepper.distanceToGo()==0) 
  {
    stepper.moveTo(-(stepper.currentPosition()));
    stepper.setSpeed(velocidad);
  }
  while (stepper.distanceToGo()!=0)
  {
  stepper.runSpeedToPosition();
  } 
}
}
