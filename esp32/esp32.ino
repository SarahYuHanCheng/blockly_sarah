/* Receive the controlling message, turning on/off and pwm, and
 * than set the corresponding pin.
 */

#include <WiFi.h>
#include "TCS3200.h"

#define SSID "scream"
#define PASSWD "s741852scream"
#define TCP_IP "192.168.1.179"
#define TCP_PORT 17784

WiFiClient wifiClient;
static char buf[32];
static int messageLen;


static char buffer[256];
static char _buffer[256];
static int char_count = 0;
String temp="";
String out_to_uno="";
int the_end=0;
byte uno_busy=0;


enum MotorPinID {
    L_F = 0,
    L_B,
    R_F,
    R_B,
    NUM_OF_MOTOR_PIN
};
enum UltrasonicPinID {
    U_F = 0,
    U_L,
    U_R,
    NUM_OF_ULTRASONIC_PIN
};

/* Pin assignment */
// Pins cannot be used on ESP32-DevKit-C: CLK, SD0, SD1, SD2, SD3, CMD,
// SVN, SVP, EN, 2, 0, 32, 33, 34, 35
// TXD0 and RXD0 are similar to the pin 0 and 1 on Arduino.
static const uint8_t motorPins[NUM_OF_MOTOR_PIN] = {22, 23, 32, 33};  //  L_F, L_B,R_F, R_B
static const uint8_t usTrigPins[NUM_OF_ULTRASONIC_PIN] = {19, 17, 21 };  // F, L, R
static const uint8_t usEchoPins[NUM_OF_ULTRASONIC_PIN] = {18, 16, 4 };  // F, L, R
TCS3200 colorSensor(25, 26, 27, 14, 12);  // S0, S1, S2, S3, Out

long ultrasonicGetDistance(uint8_t trig, uint8_t echo)
{
    long duration;

    pinMode(trig, OUTPUT);
    digitalWrite(trig, LOW);
    delayMicroseconds(2);
    digitalWrite(trig, HIGH);
    delayMicroseconds(5);
    digitalWrite(trig, LOW);

    pinMode(echo, INPUT);
    duration = pulseIn(echo, HIGH, 5000000L);
    return duration / 29 / 2;
}

void reportUltrasonic()
{
    long dF, dL, dR;

    dF = ultrasonicGetDistance(usTrigPins[U_F], usEchoPins[U_F]);
    dL = ultrasonicGetDistance(usTrigPins[U_L], usEchoPins[U_L]);
    dR = ultrasonicGetDistance(usTrigPins[U_R], usEchoPins[U_R]);

    sprintf(buf, "F:%ld cm, L:%ld cm, R:%ld cm", dF, dL, dR);
    wifiClient.write(buf, strlen(buf));
    wifiClient.flush();
}

void reportColorSensor()
{
  sprintf(buf, "R: %ld, G: %ld, B: %ld",
      colorSensor.getPeriod(RED),
      colorSensor.getPeriod(GREEN),
      colorSensor.getPeriod(BLUE));
  wifiClient.write(buf, strlen(buf));
  wifiClient.flush();
}

void handleCommand()
{
    // Stop moving
    if (buf[1] == 'E') {
        ledcWrite(L_F, 0);
        ledcWrite(L_B, 0);
        ledcWrite(R_F, 0);
        ledcWrite(R_B, 0);
        return;
    }

    switch (buf[0]) {
    case 'F':   // Forward
        ledcWrite(L_F, 180);
        ledcWrite(L_B, 0);
        ledcWrite(R_F, 180);
        ledcWrite(R_B, 0);
        break;
    case 'B':   // Backward
        ledcWrite(L_F, 0);
        ledcWrite(L_B, 180);
        ledcWrite(R_F, 0);
        ledcWrite(R_B, 180);
        break;
    case 'L':   // Turn left
        ledcWrite(L_F, 0);
        ledcWrite(L_B, 180);
        ledcWrite(R_F, 180);
        ledcWrite(R_B, 0);
        break;
    case 'R':   // Turn right
        ledcWrite(L_F, 180);
        ledcWrite(L_B, 0);
        ledcWrite(R_F, 0);
        ledcWrite(R_B, 180);
        break;
    case 'Z':   // Report ultrasonic distance and color
        reportUltrasonic();
    reportColorSensor();
        break;
    }
}

void initialPins()
{
  // Attach pins to the PWM controller.
    ledcAttachPin(motorPins[L_F], L_F);
    ledcAttachPin(motorPins[L_B], L_B);
    ledcAttachPin(motorPins[R_F], R_F);
    ledcAttachPin(motorPins[R_B], R_B);
    ledcSetup(L_F, 10000, 8);   // 10kHz, 8 bit resolution
    ledcSetup(L_B, 10000, 8);   // 10kHz, 8 bit resolution
    ledcSetup(R_F, 10000, 8); // 10kHz, 8 bit resolution
    ledcSetup(R_B, 10000, 8); // 10kHz, 8 bit resolution
    ledcWrite(L_F, 0);
    ledcWrite(L_B, 0);
    ledcWrite(R_F, 0);
    ledcWrite(R_B, 0);
}

void pop_from_queue(){
    the_end = temp.indexOf('@',0);
            if(the_end>1){
              uno_busy=1;
              out_to_uno = temp.substring(0,the_end);
              Serial.print("the outtouno:");
              Serial.println(out_to_uno);//can not send all instraction
              temp = temp.substring(the_end+1);
              Serial.println("the temp:");
              Serial.print(temp);
              }else{
              uno_busy=0;
              Serial.println("the_queue is clear");
            }
  }



void setup()
{
    initialPins();
  colorSensor.setOutFreqScaling(PERCENT_100);
    
    WiFi.mode(WIFI_STA);
    WiFi.begin(SSID, PASSWD);
    while (WiFi.waitForConnectResult() != WL_CONNECTED) {
        // Connect failed, blink 0.5 second to indicate
        // the board is retrying.
        delay(500);
        WiFi.begin(SSID, PASSWD);
    }

    // Conenct to AP successfully
    wifiClient.connect(TCP_IP, TCP_PORT);

  Serial.begin(9600);
  while (!Serial)
    ;
}

void loop()
{
    if ((messageLen = wifiClient.available()) > 0) {
        for (int i = 0; i < messageLen; ++i)
            buf[i] = wifiClient.read();
        buf[messageLen] = '\0';
//        handleCommand();
        temp+=buf;
        temp+='@';
        if(uno_busy==0){
          pop_from_queue();
          }
    }
    if ((char_count = Serial.available()) > 0) {
        int i;
        memset(_buffer, 0, 256);
        for (i = 0; i < char_count; ++i)
            _buffer[i] = Serial.read();
        _buffer[i] = '\0';
        if (strstr(_buffer, "done")) {
           
              pop_from_queue();
        }
        else if (strstr(_buffer, "end")) {
            wifiClient.stop();
            while (1)
                ;
        }
        else {
          wifiClient.write(_buffer, char_count);
          wifiClient.flush();
        }
        for(int j=0;j<char_count+1;j++){ _buffer[j]={0};}
    }

}
