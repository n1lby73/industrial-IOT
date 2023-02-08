#include <ESP8266WiFi.h>

int dt_out = 25;

#define ssid "esp8266"
#define password "forTheLoveOfEmbededSystem"

#define host "192.168.11.87" //host subject to change always untill app is hosted
int port = 3565;

void setup(){ 

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.begin (115200);
  
  while (WiFi.status() != WL_CONNECTED) {

     delay(dt);
     Serial.print(".");

  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  
}

void loop() {

//   Use WiFiClient class to create TCP connections

  WiFiClient client;

  if (!client.connect(host, port)) {

    Serial.println("connection failed");
    delay(5000);
    return;

  }  
  
  client.println("GET / HTTP/1.1");
  client.println("Host: 127.0.0.1:3333");
  client.println();

  // Read the response from the server
  while (client.available()) {
    String line = client.readStringUntil('\n');
    Serial.println(line);
  }
}