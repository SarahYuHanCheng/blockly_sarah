#include <SoftwareSerial.h>
#include "pitches.h"

SoftwareSerial mySerial(2,3);  // (RX, TX)
void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);

}
static char _buffer[512];
static int char_count = 0;
String str_buffer="";
bool isCmdStart=false;
bool isCmdEnd=false;
String arduino_uno_cmdStart = "arduinouno#####";
String arduino_uno_cmdEnd = "arduinounoend##";
String blockly_cmd="";
void loop() {
  // put your main code here, to run repeatedly:
//  if (mySerial.available() > 0) {
//
//    byte incomingByte = mySerial.read();
//    Serial.write(incomingByte);
//
//  }
    if ((char_count = mySerial.available()) > 0) {
        int i;
        for (i = 0; i < char_count; ++i)
            _buffer[i] = mySerial.read();
        _buffer[i] = '\0';
        //Serial.println(_buffer);
        str_buffer += _buffer;
        for(int i=0;i<sizeof(_buffer);i++){ _buffer[i]={0}; }
        Serial.println(str_buffer);
        if(str_buffer.indexOf(arduino_uno_cmdStart)!=-1){
              str_buffer = str_buffer.substring(str_buffer.indexOf(arduino_uno_cmdStart)+16,str_buffer.length()-1);
              isCmdStart=true;
              isCmdEnd=false;
              Serial.println("cmdStart");
        }
        if(isCmdStart){
          Serial.println("blockly_cmd:" + str_buffer);
          blockly_cmd = str_buffer;
          if(blockly_cmd.indexOf("tone")!=-1){
            int tonePin=0,toneDuration=0;
            String toneMusicName="" ;
            int doremi[]= {NOTE_C5, NOTE_D5, NOTE_E5, NOTE_F5, NOTE_G5, NOTE_A5, NOTE_B5, NOTE_C6};
            int bee[] = {NOTE_G5, NOTE_E5, NOTE_E5, 0, NOTE_F5, NOTE_D5, NOTE_D5, 0, NOTE_C5, NOTE_D5, NOTE_E5, NOTE_F5, NOTE_G5, NOTE_G5, NOTE_G5};
            int mouse_1 = blockly_cmd.indexOf("@");
            int mouse_2 = blockly_cmd.indexOf("@",mouse_1+1);
            int mouse_3 = blockly_cmd.indexOf("@",mouse_2+1);
            int mouse_4 = blockly_cmd.indexOf("@",mouse_3+1);
            tonePin = blockly_cmd.substring(mouse_1+1,mouse_2).toInt();
            toneMusicName = blockly_cmd.substring(mouse_2+1,mouse_3);
            toneDuration = blockly_cmd.substring(mouse_3+1,mouse_4).toInt();
            Serial.println("tonePin:" + String(tonePin));
            Serial.println("toneMusic:" + toneMusicName);
            Serial.println("toneDuration:" + String(toneDuration));
            if(toneMusicName.indexOf("doremi")!=-1){
              Serial.println("music:doremi");
              for (int thisNote = 0; thisNote < 8; thisNote++) {
                tone(tonePin,doremi[thisNote], toneDuration);
                delay(500);

              }
              blockly_cmd="";
              tonePin=0;
              toneMusicName="";
              toneDuration=0;
              isCmdStart=false;
            }else if(toneMusicName.indexOf("bee")!=-1){
              Serial.println("music:bee");
              for (int thisNote = 0; thisNote < 15; thisNote++) {
                tone(tonePin,bee[thisNote], toneDuration);
                delay(500);

              }
              blockly_cmd="";
              tonePin=0;
              toneMusicName="";
              toneDuration=0;
              isCmdStart=false;
            }


          }

        }

//        if(str_buffer.indexOf(arduino_uno_cmdEnd)!=-1){
//             isCmdStart=false;
//             isCmdEnd=true;
//             Serial.println("cmdEnd");
//        }


    }
}
