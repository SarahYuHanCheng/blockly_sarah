#include <ESP8266WiFi.h>
#include <WiFiClient.h>


#define TCP_PORT 17784
#define SSID "scream"
#define PASSWD "s741852scream"
#define TCP_IP "192.168.1.179"

WiFiClient wifiClient;

void setup()
{

    Serial.begin(9600);
    while (!Serial)
        ;
    Serial.println("Connecting...");
    WiFi.mode(WIFI_STA);
    WiFi.begin(SSID, PASSWD);
    while (WiFi.waitForConnectResult() != WL_CONNECTED) {
        WiFi.begin(SSID, PASSWD);
        Serial.println("Retrying...");
    }
    Serial.println("Connected to AP");
    wifiClient.connect(TCP_IP, TCP_PORT);
    while(true){
      if(!wifiClient.connected()){
       wifiClient.connect(TCP_IP, TCP_PORT);
       Serial.println("Trying connect to TCP server:"+String(TCP_IP)+" "+String(TCP_PORT));
      }
      else{
        Serial.println("Successful connect to TCP server:"+String(TCP_IP)+" "+String(TCP_PORT));
        break;
      }
    }
}
void pop_from_queue(){
    the_end = temp.indexOf('@',0);
            if(the_end>1){
              uno_busy=1;
              out_to_uno = temp.substring(0,the_end);
              Serial.println(out_to_uno);//can not send all instraction
              temp = temp.substring(the_end+1);
              Serial.println(temp);
//              return out_to_uno;
              }else{
              uno_busy=0;
//              return "";
            }
  }

static char buffer[256];
static char _buffer[256];
static char _Instras[256];
static int char_count = 0;
String temp="";
String out_to_uno="";
int the_end=0;
byte uno_busy=0;
void loop()
{
    // Receive the message sent from Arduino IDE
    // and send to TCP server
    if ((char_count = Serial.available()) > 0) {
        int i;
        memset(_buffer, 0, 256);
        for (i = 0; i < char_count; ++i)
            _buffer[i] = Serial.read();
        _buffer[i] = '\0';
//        wifiClient.write(_buffer, char_count);
//        wifiClient.flush();
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
        for(int j=0;j<sizeof(buffer);j++){ buffer[j]={0};}
    }
    // Receive the message sent from TCP server
    // and send to Arduino IDE
    if ((char_count = wifiClient.available()) > 0) {
        wifiClient.read((unsigned char *)buffer, 256);
        temp+=buffer;
        temp+='@';
        if(uno_busy==0){
          pop_from_queue();
          Serial.print(temp);
          uno_busy=1;
          }
//        Serial.print(temp);
        for(int j=0;j<sizeof(buffer);j++){ buffer[j]={0};};
    }
}
