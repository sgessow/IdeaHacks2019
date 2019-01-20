#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>

#define wifi_ssid "ESP"
#define wifi_password "sammygphone"

#define mqtt_topic "rangefinder_data"
//#define mqtt_server "broker.mqttdashboard.com" //global
#define mqtt_server "192.168.43.21"

const int trig_pin=0;
const int echo_pin=2;

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
     pinMode(trig_pin,OUTPUT); 
     pinMode(echo_pin,INPUT); 
}
void loop () // Code under this loop runs forever.
{
    float duration, distance;
    digitalWrite(trig_pin, LOW); 
    delayMicroseconds(2);
 
    digitalWrite(trig_pin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trig_pin, LOW);
  
    duration = pulseIn(echo_pin, HIGH);
    distance = (duration / 2) * 0.0344;
    if (distance<1000){
      Serial.println(distance);
      String toSend="{distance:"+String(distance)+"}";
       if (!client.connected()) {
          reconnect();
       }
      client.loop();
      client.publish(mqtt_topic, toSend.c_str(), true);
      delay(50); 
    }
}
