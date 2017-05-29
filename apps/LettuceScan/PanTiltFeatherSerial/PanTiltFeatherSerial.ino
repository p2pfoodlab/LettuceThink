#include "parser.hpp"

#define USE_AFMS 0

/******************* Adafruit Motorshield **********************/
#if USE_AFMS
#include <Adafruit_MotorShield.h>
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
Adafruit_StepperMotor *TiltMotor = AFMS.getStepper(200, 2);
Adafruit_StepperMotor *PanMotor = AFMS.getStepper(200, 1);

int currentPan = 0;
int currentTilt = 0;
int mode = DOUBLE; //SINGLE 1, DOUBLE 2, INTERLEAVE 3, MICROSTEP 4

void initSteppers()
{
  AFMS.begin();
  TiltMotor->setSpeed(50);    
  PanMotor->setSpeed(50);   
  TiltMotor->step(0, FORWARD, mode);
  PanMotor->step(0, FORWARD, mode); 
}

void setSpeed(int s)
{
  TiltMotor->setSpeed(s);    
  PanMotor->setSpeed(s);  
}

void setMode(int value)
{
  mode = value;
}

void setPan(int value)
{
  int step10 = map(value, -1800, 1800, -2000, 2000);
  int step = (step10 + 5) / 10;
  int delta = (step - currentPan);
  PanMotor->step(abs(delta), (delta > 0)? FORWARD : BACKWARD, mode);
  currentPan = step;
}

int getPan()
{
  return map(currentPan, -200, 200, -1800, 1800);
}

void setTilt(int value) 
{
  int step10 = map(value, -1800, 1800, -2000, 2000);
  int step = (step10 + 5) / 10;
  int delta = (step - currentTilt);
  TiltMotor->step(abs(delta), (delta > 0)? FORWARD : BACKWARD, mode);
  currentTilt = step;
}

int getTilt()
{
  return map(currentTilt, -200, 200, -1800, 1800);
}

void updateSteppers()
{
}

/*************** AccelStepper ********************/
#else 

#include <AccelStepper.h>
#define FULLSTEPS_PER_TURN  200
#define FULLSTEPS_PER_TURN_10  2000
int mode = 2; // 1=fullstep, 2=half-step, 4=1/4-step, 8=1/8-step
AccelStepper pan(AccelStepper::DRIVER, 9, 10);
AccelStepper tilt(AccelStepper::DRIVER, 5, 6);

void initSteppers()
{
  pan.setMaxSpeed(200);
  pan.setAcceleration(200);
  tilt.setMaxSpeed(500);
  tilt.setAcceleration(200);
}

void setSpeed(int s)
{
  // TODO: should set speed seperately for pan and tilt
  pan.setMaxSpeed(s);
  tilt.setMaxSpeed(s);
}

void setMode(int value)
{
   mode = value;
}

void setPan(int value)
{
  int step10 = map(value, -1800, 1800, -FULLSTEPS_PER_TURN_10 * mode, FULLSTEPS_PER_TURN_10 * mode);
  int step = (step10 + 5) / 10;
  pan.moveTo(step);
}

int getPan()
{
  return map(pan.currentPosition(), -FULLSTEPS_PER_TURN * mode, FULLSTEPS_PER_TURN * mode, -1800, 1800);
}

void setTilt(int value) 
{
  int step10 = map(value, -1800, 1800, -FULLSTEPS_PER_TURN_10 * mode, FULLSTEPS_PER_TURN_10 * mode);
  int step = (step10 + 5) / 10;
  tilt.moveTo(step);
}

int getTilt()
{
   return map(tilt.currentPosition(), -FULLSTEPS_PER_TURN * mode, FULLSTEPS_PER_TURN * mode, -1800, 1800);
}

void updateSteppers()
{
  pan.run();
  tilt.run();
}

#endif


/********************************************************/

Parser serialParser = Parser();

void setup() 
{
  Serial.begin(9600);             
  initSteppers();
}

void handleCommand(Parser& p) 
{
  switch (p.opcode) {
    case 'p': 
      setPan(p.value);
      break; 
    case 't': 
      setTilt(p.value);
      break;
    case 'm': 
      setMode(p.value);
      break;
    case 's': 
      setSpeed(p.value);
      break;
  }
  Serial.print(getPan());
  Serial.print(",");
  Serial.println(getTilt());
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
  updateSteppers();
}

