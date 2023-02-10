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
int wifiDt = 100;

int motor  = 26;
int motorPb = 27;
int pbStateOld;
int pbStateNew;
int localMotorState;
int motorState;
int globalState;

int syncSuccess;
#define ssid "esp8266"
#define password "forTheLoveOfEmbededSystem"

const char* serverIP = "192.168.170.87"; //host subject to change always untill app is hosted
const int serverPort = 3565; 

// Function to constantly check for changes on the hardware

void hardChanges(){

  pbStateNew = digitalRead(motorPb);

  if ((pbStateNew == 1) && (pbStateOld == 0)) {

    if (localMotorState == 0) {

      digitalWrite(motor, HIGH);
      localMotorState = 1;
      globalState = 1;

    }

    else {

      digitalWrite(motor, LOW);
      localMotorState = 0;
      globalState = 0;

    }
  }

  pbStateOld = pbStateNew;

}

void syncHardChanges(){

  DynamicJsonDocument doc(200);
  doc["state"] = localMotorState;
  doc["pin"] = 5;

  String jsonString;
  serializeJson(doc, jsonString);

  HTTPClient http;
  WiFiClient client;

  String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/synchardchanges";

  http.begin(client, url);
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.POST(jsonString);

  if (httpCode > 0){
    // pass;
    // motorState = localMotorState;

  }

  http.end();

}

void setup(){ 

  pinMode(motor, OUTPUT);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.begin (115200);
  
  while (WiFi.status() != WL_CONNECTED) {

     Serial.print("Connecting to Wifi network...");
     Serial.println(".");

     hardChanges();
     Serial.println(localMotorState);

  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  
}

void loop() {
  
  Serial.print("Inside the loop: ");
  Serial.println(localMotorState);
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
      Serial.print("got here ==> ");
      Serial.println(motorState);
      // if (localMotorState == 1){
      if (motorState != localMotorState){

        // motorState = doc["success"];
        Serial.print("got here 2==> ");
        Serial.println(motorState);
        syncHardChanges();
        Serial.print("new motor: ");
        Serial.println(motorState);

        if (globalState == 0){

          if ((motorState == 1) || (localMotorState == 1)){

              digitalWrite(motor, HIGH);
              globalState = 1;
              return;

          }
        }

        else {

          if ((motorState == 0) || (localMotorState == 0)){

              digitalWrite(motor, LOW);
              globalState = 0;
              return;

          }

        }
        
        delay(2000);
        // return;

      }

      if (motorState == 1){
        Serial.println("this block");
        digitalWrite(motor, HIGH);
        globalState = 1;

      }

      else{
        Serial.println("this block2");
        Serial.println("");
        digitalWrite(motor, LOW);
        globalState = 0;

      }

    }

    else{

      Serial.println("Error: " + String(httpCode));

    }

    http.end();
    delay(1000);
  }

  else{

    Serial.println("Wifi disconnected");
    delay(wifiDt);

    while (WiFi.status() != WL_CONNECTED) {

      delay(wifiDt);
      Serial.println("Reconnecting to "+String(ssid)+" wifi network....");

      hardChanges();

    }

    Serial.println("Connected to "+String(ssid));
    syncHardChanges();

  }

  delay (dt_out);

}
