#include <AccelStepper.h>
#include <Ethernet2.h>

byte mac[] = {
  //0x98, 0x76, 0xB6, 0x10, 0x57, 0x70
  //0x98, 0x76, 0xB6, 0x10, 0x61, 0xC9
  0x98, 0x76, 0xB6, 0x10, 0x61, 0xBE
};
IPAddress ip(10, 20, 30, 40);
EthernetServer server(10101);


void setup() {
  Serial.begin(115200);
  
  // start the Ethernet connection and the server:
  Serial.println("Ethernet.begin");
  Ethernet.begin(mac, ip);
  server.begin();
  Serial.print("server is at ");
  Serial.println(Ethernet.localIP());
}

enum _pstatus {
  _opcode = 0,
  _sign_or_digit = 1,
  _digit = 2
};

int pstate = _opcode;
int opcode = 0;
int sign = 1;
int value = 0;

void loop() 
{
  EthernetClient client = server.available();
  if (client) {
     while (client.available()) {
        char c = client.read();
        Serial.write(c);
        if (c == 'p') { 
          if (pstate == _opcode) {
            opcode = 'p';
            pstate = _sign_or_digit;
            value = 0;
          } else pstate = _opcode;
        } else if (c == 't') { 
          if (pstate == _opcode) {
            opcode = 't';
            pstate = _sign_or_digit;
            value = 0;
          } else pstate = _opcode;
          break;
        } else if (c == '-') {
          if (pstate == _sign_or_digit) {
            sign = -1;
            pstate = _digit;
          } else pstate = _opcode; 
        } else if (c >= '0' && c <= '9') {
          if (pstate == _sign_or_digit) {
            sign = 1;
            value = c - '0';
            pstate = _digit;
          } else if (pstate == _digit) {
            value = value * 10 + (c - '0');
          } else pstate = _opcode; 
        } else if (c == ';') {
          if (pstate == _digit) {
            value = sign * value;
            if (opcode == 'p') 
              setPan(value);
            else if (opcode == 't') 
              setTilt(value);
            pstate = _opcode;
          } else pstate = _opcode; 
        } else {
          pstate = _opcode;
        }
     }
  }
}

void setPan(int v)
{

}

void setTilt(int v)
{

}

