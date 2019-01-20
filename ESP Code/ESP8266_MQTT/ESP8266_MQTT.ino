#include <SparkFun_ADXL345.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>

//
ADXL345 adxl = ADXL345();       


#define wifi_ssid "ESP"
#define wifi_password "sammygphone"

#define mqtt_topic "rangefinder_data"
//#define mqtt_server "broker.mqttdashboard.com" //global
#define mqtt_server "192.168.43.21"


WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(wifi_ssid);

  WiFi.begin(wifi_ssid, wifi_password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    Serial.print(WiFi.status());
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) {
 
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
 
  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
 
  Serial.println();
  Serial.println("-----------------------");
 
}

void setup ()  
{
     Serial.begin(9600);
     setup_wifi();
     client.setServer(mqtt_server, 1883);
     client.setCallback(callback);
     Wire.begin(0,2);
     adxl.powerOn(); 
}
void loop () // Code under this loop runs forever.
{
    int x,y,z;
    adxl.readAccel(&x, &y, &z);
    String toSend="{{source: 'accl'},{x:"+String(x)+", y:"+String(y)+", z:"+String(z)+"}}";
    Serial.print(x);
    Serial.print(", ");
    Serial.print(y);
    Serial.print(", ");
    Serial.println(z); 
     if (!client.connected()) {
        reconnect();
     }
    client.loop();
    client.publish(mqtt_topic, toSend.c_str(), true);
    delay(500); 
}
