#define encoder0PinA  2
#define encoder0PinB  4

volatile long encoder0Pos = 0;

void setup()
{ 
  Serial.begin(9600);

  pinMode(encoder0PinA, INPUT); 
  digitalWrite(encoder0PinA, HIGH);       // turn on pull-up resistor
  pinMode(encoder0PinB, INPUT); 
  digitalWrite(encoder0PinB, HIGH);       // turn on pull-up resistor
  EICRA |= 0x03;  //select rising edge on INT0 (digital 2)
  EIMSK |= 0x01;  //enable INT0 interrupts
}

void loop()
{
  Serial.println(encoder0Pos);
  delay(1000);
}

SIGNAL(INT0_vect)
{
  //Port D pin 2 is high since this is a rising interrupt
  if (PIND & 0x10)    //if pin 4 is also high
    encoder0Pos++;    //encoder is moving forward
  else
    encoder0Pos--;    //encoder is moving backward
}



