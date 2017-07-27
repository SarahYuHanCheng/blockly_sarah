#include <SoftwareSerial.h>
#include <Servo.h>
SoftwareSerial mySerial(2,3);  // (RX, TX)
#define ultrasonicPin 5
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
long ultrasoundGet()
{
  long duration;
  pinMode( ultrasonicPin, OUTPUT );
  digitalWrite( ultrasonicPin, LOW );
  delayMicroseconds(2);
  digitalWrite( ultrasonicPin, HIGH );
  delayMicroseconds(5);
  digitalWrite( ultrasonicPin, LOW );

  pinMode( ultrasonicPin, INPUT );
  duration = pulseIn( ultrasonicPin, HIGH );

  return duration / 29 / 2;
  }
void ddd(int sec){
  delay(sec);
//  mySerial.println();
  }

void loop() {

  long distance = ultrasoundGet();
  
  if ((char_count = mySerial.available()) > 0) {
        String bf="";
        byte the_func;
        int i;
        for (i = 0; i < char_count; ++i){
            _buffer[i] = mySerial.read();
        }
        _buffer[i] = '\0';
//        Serial.print(_buffer);
        bf+=_buffer;
        
        the_func = _buffer[0];//'u';
        Serial.println(_buffer);
        for(int j=0;j<i;j++){ _buffer[j]={0}; }
          switch (the_func) {
            case 'U': // ultrasound set
//                  int i_trigpin = bf.indexOf("#",2);
//                  int i_echopin = bf.indexOf("#",i_trigpin+1);
//                  ultrasonicPin =bf.substring(2,i_trigpin).toInt();
//                  ultrasound(i_trigpin,i_echopin);      
              break;
            case 'u':// ultrasound get
//                  mySerial.print(u_distance);
                    mySerial.println(distance);
                    
                    ddd(20000);
                    mySerial.println("done");
                    Serial.println("send distance");
              break;
              case'M'://motor
//                  int i_pin = bf.indexOf("#",2);
//                  int i_pin2 = bf.indexOf("#",i_pin+1);
//                  pin_msg=bf.substring(2,i_pin).toInt();
//                  angle_msg=bf.substring(i_pin2+1,i).toInt();
//                  myservo.attach(pin_msg);
//                  myservo.write(angle_msg); //tell servo to go to position
            default: 
              // if nothing else matches, do the default
              // default is optional
            break;
  }
  
  }
}
