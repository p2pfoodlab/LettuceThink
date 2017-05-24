#include <Adafruit_MotorShield.h>
#include "parser.hpp"

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *TiltMotor = AFMS.getStepper(200, 2);
Adafruit_StepperMotor *PanMotor = AFMS.getStepper(200, 1);

Parser serialParser = Parser();

int currentPan = 0;
int currentTilt = 0;
int mode = DOUBLE; //SINGLE 1, DOUBLE 2, INTERLEAVE 3, MICROSTEP 4

void setSpeed(int s)
{
  TiltMotor->setSpeed(s);    
  PanMotor->setSpeed(s);  
}

void setup() 
{
  Serial.begin(9600);             
  AFMS.begin();
 
  TiltMotor->setSpeed(50);    
  PanMotor->setSpeed(50);  
 
  TiltMotor->step(0, FORWARD, mode);
  PanMotor->step(0, FORWARD, mode); 
}

void setPan(int value) 
{
  int step10 = map(value, -1800, 1800, -2000, 2000);
  int step = (step10 + 5) / 10;
  int delta = (step - currentPan);
  PanMotor->step(abs(delta), (delta > 0)? FORWARD : BACKWARD, mode);
  currentPan = step;
}

void setTilt(int value) 
{
  int step10 = map(value, -1800, 1800, -2000, 2000);
  int step = (step10 + 5) / 10;
  int delta = (step - currentTilt);
  TiltMotor->step(abs(delta), (delta > 0)? FORWARD : BACKWARD, mode);
  currentTilt = step;
}

void handleCommand(Parser& p) 
{
  Serial.print("#Command: opcode=");
  Serial.print(p.opcode);
  Serial.print(", value=");
  Serial.println(p.value);
  switch (p.opcode) {
    case 'p': 
      setPan(p.value);
      break; 
    case 't': 
      setTilt(p.value);
      break;
    case 'm': 
      mode = p.value;
      break;
    case 's': 
      setSpeed(p.value);
      break;
  }
}

void loop()
{
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (serialParser.handle(c) == COMMAND) {
      handleCommand(serialParser);
    }
    delay(1);
  }
  delay(10);
}

