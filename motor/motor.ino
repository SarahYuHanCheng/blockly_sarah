#include <SoftwareSerial.h>
#include <Servo.h>
SoftwareSerial mySerial(2,3);  // (RX, TX)
Servo myservo;
int trigpin = 9;
int echopin = 10;
void ultrasound(int new_trigpin,int new_echopin){
  trigpin=new_trigpin;
  echopin=new_echopin;
  pinMode(trigpin, OUTPUT);
  pinMode(echopin, INPUT); 
  }
void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
}
static char _buffer[512];
static int char_count = 0;
long duration;
int pin_msg, angle_msg, u_distance;

void loop() {

  digitalWrite(trigpin,LOW);
  delayMicroseconds(2);
  digitalWrite(trigpin,HIGH);
  delayMicroseconds(10);
  digitalWrite(trigpin,LOW);
  duration = pulseIn(echopin,HIGH);
  u_distance =duration*0.034/2;
  Serial.print(distance);
  Serial.println("cm");

  if ((char_count = mySerial.available()) > 0) {
        String bf="";
        char the_func;
        int i;
        for (i = 0; i < char_count; i++){
            _buffer[i] = mySerial.read();
        }
        _buffer[i] = '\0';
        Serial.print(_buffer);
        bf+=_buffer;
        for(int j=0;j<sizeof(_buffer);j++){ _buffer[j]={0}; }
//        int i_func = bf.indexOf("#");
//        the_func=bf.substring(0,i_func);
          the_func = _buffer[0];
          switch (the_func) {
            case 'U': // ultrasound set
                  int i_trigpin = bf.indexOf("#",i_func+1);
                  int i_echopin = bf.indexOf("#",i_trigpin+1);
                  ultrasound(i_trigpin,i_echopin);
                  
              break;
            case 'u':// ultrasound get
                  mySerial.print(u_distance);
              break;
              case'M'://motor
                  int i_trigpin = bf.indexOf("#",i_func+1);
                  int i_echopin = bf.indexOf("#",i_trigpin+1);
                  pin_msg=bf.substring(0,i_pin).toInt();
                  angle_msg=bf.substring(i_pin+1,i).toInt();
                  myservo.attach(pin_msg);
                  myservo.write(angle_msg); //tell servo to go to position
            default: 
              // if nothing else matches, do the default
              // default is optional
            break;
  }
  }
  if(digitalRead(8)){
    mySerial.print("pressed");
     Serial.println("pressed");
  }
}
