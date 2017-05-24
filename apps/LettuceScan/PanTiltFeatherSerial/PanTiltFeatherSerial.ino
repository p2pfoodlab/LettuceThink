#include <Adafruit_MotorShield.h>
#include "parser.hpp"

Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *TiltMotor = AFMS.getStepper(200, 2);
Adafruit_StepperMotor *PanMotor = AFMS.getStepper(200, 1);

Parser serialParser = Parser();

int pan = 0;
int tilt = 0;
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

void handleCommand(Parser& p) 
{
  switch (p.opcode) {
    Serial.print("#Command: opcode=");
    Serial.print(p.opcode);
    Serial.print(", value=");
    Serial.println(p.value);
    case 'p': 
      PanMotor->step(p.absvalue, (p.sign == 1)? FORWARD : BACKWARD, mode);
      pan += p.value;
      break; 
    case 't': 
      TiltMotor->step(p.absvalue, (p.sign == 1)? FORWARD : BACKWARD, mode);
      tilt += p.value;
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
  }
}

