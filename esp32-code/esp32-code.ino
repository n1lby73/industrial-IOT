#include <ESP8266WiFi.h>

int dt = 500;

#define ssid "esp8266"
#define password "stancyleemallstancy"

#define host "192.168.47.87"
int port = 3565;

WiFiClient client;

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
  Serial.println(WiFi.localIP());

  if (!client.connect(host,port)) {
    Serial.println("Connection to server failed");
    return;
  }
  Serial.println("Connected to server");
  
}

void loop() {
  
  client.println("GET / HTTP/1.1");
  client.println("Host: 127.0.0.1:3333");
  client.println();

  // Read the response from the server
  while (client.available()) {
    String line = client.readStringUntil('\n');
    Serial.println(line);
  }
}
