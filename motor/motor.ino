#include <SoftwareSerial.h>
#include <Servo.h>
SoftwareSerial mySerial(2,3);  // (RX, TX)
Servo myservo;
void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  pinMode(8, INPUT);
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(13, OUTPUT);
}
static char _buffer[512];
static int char_count = 0;

int pin_msg;
int angle_msg;
void loop() {
  
  if ((char_count = mySerial.available()) > 0) {
        String bf="";
        int i;
        for (i = 0; i < char_count; i++){
            _buffer[i] = mySerial.read();
        }
        _buffer[i] = '\0';
        Serial.print(_buffer);
        bf+=_buffer;
        for(int j=0;j<sizeof(_buffer);j++){ _buffer[j]={0}; }
        int i_pin = bf.indexOf("#");
        pin_msg=bf.substring(0,i_pin).toInt();
        angle_msg=bf.substring(i_pin+1,i).toInt();
        myservo.attach(pin_msg);
//        analogWrite(pin_msg,angle_msg);
        myservo.write(angle_msg);              // tell servo to go to position in variable 'pos'
        delay(15);
  }
  delay(100);
  if(digitalRead(8)){
    mySerial.print("pressed");
     Serial.println("pressed");
  }
}
