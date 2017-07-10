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

static char buffer[256];
static char _buffer[256];
static int char_count = 0;

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

        wifiClient.write(_buffer, char_count);
        wifiClient.flush();
        if (strstr(_buffer, "end")) {
            wifiClient.stop();
            while (1)
                ;
        }
    }
    // Receive the message sent from TCP server
    // and send to Arduino IDE
    if ((char_count = wifiClient.available()) > 0) {
        wifiClient.read((unsigned char *)buffer, 256);
        Serial.println(buffer);
        for(int j=0;j<sizeof(buffer);j++){ buffer[j]={0}; }
    }
}
