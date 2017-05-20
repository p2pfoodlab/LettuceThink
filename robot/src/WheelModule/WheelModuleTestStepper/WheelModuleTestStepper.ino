#include <AccelStepper.h>

#define DIRECTION_DIR 5
#define DIRECTION_STEP 6
#define DIRECTION_ENABLE 13

AccelStepper stepper(AccelStepper::DRIVER,  DIRECTION_STEP,  DIRECTION_DIR);

void setup()
{ 
  Serial.begin(115200);
  stepper.setMaxSpeed(4000);
  stepper.setAcceleration(2500);
  stepper.moveTo(500);
}


void loop()
{
    if (stepper.distanceToGo() == 0)
      stepper.moveTo(-stepper.currentPosition());
    stepper.run();
}


