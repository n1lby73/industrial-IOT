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

int motor  = 26;
int motorPb = 27;
int pbStateOld;
int pbStateNew;
int localMotorState;
int motorState;

int syncSuccess;
#define ssid "esp8266"
#define password "forTheLoveOfEmbededSystem"

const char* serverIP = "192.168.56.87"; //host subject to change always untill app is hosted
const int serverPort = 3565; 

// Function to constantly check for changes on the hardware

void hardChanges(){

  pbStateNew = digitalRead(motorPb);

  if ((pbStateNew == 1) && (pbStateOld == 0)) {

    if (localMotorState == 0) {

      digitalWrite(motor, HIGH);
      localMotorState = 1;

    }

    else {

      digitalWrite(motor, LOW);
      localMotorState = 0;

    }
  }

  pbStateOld = pbStateNew;

}

void syncHardChanges(){

  DynamicJsonDocument doc(200);
  doc["motorState"] = localMotorState;

  String jsonString;
  serializeJson(doc, jsonString);

  HTTPClient http;
  WiFiClient client;

  String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/syncHardChanges";

  http.begin(client, url);

  int httpCode = http.POST(jsonString);

  if (httpCode > 0){

    localMotorState = motorState;

  }

  http.end();

}

void setup(){ 

  pinMode(motor, OUTPUT);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.begin (115200);
  
  while (WiFi.status() != WL_CONNECTED) {

     delay(wifiDt);
     Serial.print("Connecting to Wifi network...");
     Serial.println(".");

     hardChanges();

  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  
}

void loop() {

  hardChanges();
  
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

      motorState = doc["success"];

      if (motorState != localMotorState){

        syncHardChanges();
        return;

      }

      if (motorState == 1){

        digitalWrite(motor, HIGH);

      }

      else{

        digitalWrite(motor, LOW);

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

      hardChanges();

    }

    Serial.println("Connected to "+String(ssid));
    syncHardChanges();

  }

  delay (dt_out);

}
