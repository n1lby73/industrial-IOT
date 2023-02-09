/*
  Refrence:
    WiFiClient (Arduino pre-built example)
    WiFiClientBasic (Arduino pre-built exaample)
    Httpclient (Arduino pre-built example)
    
*/

#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <WiFi.h>

int dt_out = 25; //dt_out ==> delay timer out (out denoting the end of the void loop)
int minDt = 0.5; //minDt ==> minimum timer
int wifiDt = 5000;

int eMotorStartPin  = 26;

#define ssid "esp8266"
#define password "forTheLoveOfEmbededSystem"

const char* serverIP = "192.168.70.87"; //host subject to change always untill app is hosted
const int serverPort = 3565; 

void setup(){ 

  pinMode(eMotorStartPin, OUTPUT);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.begin (115200);
  
  while (WiFi.status() != WL_CONNECTED) {

     delay(wifiDt);
     Serial.print("Connecting to Wifi network...");
     Serial.println(".");

  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  
}

void loop() {

  // Check if wifi is connected

  if (WiFi.status() == WL_CONNECTED){

    // Use WiFiClient and HTTPclient class to create TCP connections

    HTTPClient http;
    WiFiClient client;

    String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/query";

    http.begin(client, url);

    int httpCode = http.POST("");

    if (httpCode > 0){

      String payload = http.getString();

      int json = payload.indexOf("{");
      String jsonData = payload.substring(json);

      DynamicJsonDocument doc(200);
      DeserializationError error = deserializeJson(doc, jsonData);

      if (error) {

      Serial.println("Deserialization failed: " + String(error.c_str()));
      return;

      }

      int motorState = doc["success"];

      if (motorState == 1){

        digitalWrite(eMotorStartPin, HIGH);

      }

      else{

        digitalWrite(eMotorStartPin, LOW);

      }

    }

    else{

      Serial.println("Error: " + String(httpCode));

    }

    http.end();
    
  }

  else{

    Serial.println("Wifi disconnected");
    delay(wifiDt);

    while (WiFi.status() != WL_CONNECTED) {

      delay(wifiDt);
      Serial.println("Reconnecting to "+String(ssid)+"....");

    }

    Serial.println("Connected to "+String(ssid));

  }

  delay (dt_out);

}
