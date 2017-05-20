#include <SPI.h>
#include <Ethernet2.h>

volatile int speed_value = 0;
volatile int direction_value = 0;
volatile int speed_prev_time = 0;
volatile int direction_prev_time = 0;

int last_speed = 0;
int last_direction = 0;

int INTERRUPT_SPEED = digitalPinToInterrupt(3);
int INTERRUPT_DIRECTION = digitalPinToInterrupt(2);

#define MIN_DELTA 4
#define SPEED_MIN 1632
#define SPEED_MAX 1896
#define DIR_MIN 1120
#define DIR_MAX 1920

byte mac[] = { 0x98, 0x76, 0xB6, 0x10, 0x57, 0x57 };
IPAddress ip(10, 20, 30, 2);
IPAddress server(10, 20, 30, 1);
EthernetClient client;
int wasConnected = 0;

void setup() {
  Serial.begin(115200);
  //while (!Serial)
  //  ;

  attachInterrupt(INTERRUPT_SPEED, speed_rising, RISING);
  attachInterrupt(INTERRUPT_DIRECTION, direction_rising, RISING);

  Ethernet.begin(mac, ip);
  Serial.print("IP is ");
  Serial.println(Ethernet.localIP());

  // give the Ethernet shield a second to initialize:
  delay(1000);
  Serial.println("connecting...");

  // if you get a connection, report back via serial:
  if (client.connect(server, 10101)) {
    Serial.println("connected");
    wasConnected = 1;
  }
  else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  }
}

long lastCheck = 0;

void checkConnection()
{
  if (client.connected())
    return;
  else if (wasConnected) {
    Serial.println("was connected");
    wasConnected = 0;
    int c;
    Serial.println("reading remaining data");
    while (client.available())
      c = client.read();
    Serial.println("stopping connection");
    client.stop();
  }

  long now = millis();
  if (now - lastCheck < 3000)
    return;
  lastCheck = now;

  // if you get a connection, report back via serial:
  if (client.connect(server, 10101)) {
    Serial.println("connected");
    wasConnected = 1;
  }
  else {
    // if you didn't get a connection to the server:
    Serial.println("connection failed");
  }  
}

long lastPing = 0;

void sendPing()
{
  long now = millis();
  if (now - lastPing < 1000)
    return;
  lastPing = now;
  if (client.connected()) {
      client.print('P');
      client.println(";");
  }
}

void sendSpeedAndDirection()
{
  int changed = 0;
  int delta_speed = last_speed - speed_value;
  if (delta_speed > MIN_DELTA || delta_speed < -MIN_DELTA) {
    changed = 1;
    last_speed = speed_value;
  }
  int delta_direction = last_direction - direction_value;
  if (delta_direction > MIN_DELTA || delta_direction < -MIN_DELTA) {
    changed = 1;
    last_direction = direction_value;
  }
  if (changed) {
    int speed = map(last_speed, SPEED_MIN, SPEED_MAX, 0, 100);
    int direction = map(last_direction, DIR_MIN, DIR_MAX, -90, 90);
    /*Serial.print("connected ");
    Serial.print(client.connected());
    Serial.print(" - v");
    Serial.print(speed);
    Serial.print("; d");
    Serial.print(direction);
    Serial.println(";");*/ 
    if (client.connected()) {
      client.print('v');
      client.print(speed);
      client.print(";d");
      client.print(direction);
      client.println(';');
    }
  }
}

void loop() 
{ 
  checkConnection();
  sendPing();
  sendSpeedAndDirection();  
  delay(1);
}
 
void speed_rising() {
  attachInterrupt(INTERRUPT_SPEED, speed_falling, FALLING);
  speed_prev_time = micros();
}
 
void speed_falling() {
  attachInterrupt(INTERRUPT_SPEED, speed_rising, RISING);
  speed_value = micros() - speed_prev_time;
}

void direction_rising() {
  attachInterrupt(INTERRUPT_DIRECTION, direction_falling, FALLING);
  direction_prev_time = micros();
}
 
void direction_falling() {
  attachInterrupt(INTERRUPT_DIRECTION, direction_rising, RISING);
  direction_value = micros() - direction_prev_time;
}
