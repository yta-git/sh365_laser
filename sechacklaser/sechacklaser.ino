#include <SoftwareSerial.h>

SoftwareSerial device(16, 14);

int b1, b2, safe = 'O';

void setup(){
  // put your setup code here, to run once:
  
  //button
  pinMode(10, 0);
  pinMode(18, 0);

  //LED
  pinMode(9, 1);
  pinMode(13, 1);

  //laser
  pinMode(11, 1);


  //BT
  device.begin(9600);
  Serial.begin(115200);
}

void loop(){
  // put your main code here, to run repeatedly:

  b1 = !digitalRead(10);
  b2 = !digitalRead(18);

  if(b1)      device.print('g');
  else if(b2) device.print('n');
  else        device.print('x');
  
  safe = device.read();
  
  if(safe == 'O') digitalWrite(13, 1);
  if(safe == 'X') digitalWrite(13, 0);

  if(b1 || b2){
    
    if(safe == 'O'){
      digitalWrite(9, 1);
      digitalWrite(11, 1);
    }
    
    if(safe == 'X'){
      digitalWrite(9, 0);
      digitalWrite(11, 0);
    }
    
  }else{
    digitalWrite(9, 0);
    digitalWrite(11, 0);
  }
}

