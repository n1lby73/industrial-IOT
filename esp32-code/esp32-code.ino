#include <ESP8266WiFi.h>

int dt_out = 25; //dt_out ==> delay timer out (out denoting the end of the void loop)
int dt = 5000; //dt ==> delay timer
int minDt = 0.5; //minDt ==> minimum timer

#define ssid "esp8266"
#define password "forTheLoveOfEmbededSystem"

#define host "192.168.115.87" //host subject to change always untill app is hosted
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
  
  // Make a POST request to the server

  client.println("POST / HTTP/1.1");
  client.println("Host: 127.0.0.1:3333");
  client.println();

  // Check for response from the server

  int timeOut = 0;
  
  while (client.available() && timeOut < 60000) {

    timeOut ++;
    delay(minDt);

  }

  if (client.available() > 0){
  
    String value = client.readString();
    Serial.println(value);

  }

  else{

    Serial.println("client.available() timed out ");

  }

  delay (dt_out);

}
