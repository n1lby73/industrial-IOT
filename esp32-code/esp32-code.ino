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
#define password "forTheLoveOfEmbededSystems"

const char* serverIP = "192.168.173.87"; //host subject to change always untill app is hosted
const int serverPort = 3565; 

// Function to constantly check for changes on the hardware

void hardChanges(){
  Serial.println("hardware");
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
  
  // Serial.print("Inside the loop: ");
  // Serial.println(localMotorState);
  hardChanges();

  Serial.println("");

  Serial.print("motor state @ start: ");
  Serial.println(motorState);

  Serial.print("local motor @ start: ");
  Serial.println(localMotorState);

  delay(2000);
  // Check if wifi is connected

  if (WiFi.status() == WL_CONNECTED){

    Serial.println("");

    Serial.print("motor state inside wifi: ");
    Serial.println(motorState);

    Serial.print("local motor inside wifi: ");
    Serial.println(localMotorState);

    delay(2000);

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

      Serial.println("");

      Serial.print("motor state: ");
      Serial.println(motorState);

      Serial.print("local motor: ");
      Serial.println(localMotorState);

      Serial.println("");

      delay(1000);

      // if (motorState = localMotorState){
      if (localMotorState == 1){
        Serial.println("enter");
        syncHardChanges();

        // if (motorState == 1){

        //   localMotorState = 1;

        // }

        // else{

          localMotorState = pbStateOld;

        // }
        // update globalstate
        Serial.println("");

        Serial.print("motor state after enter: ");
        Serial.println(motorState);

        Serial.print("local motor after enter: ");
        Serial.println(localMotorState);

        delay(2000);

      }

      Serial.println("");

      Serial.print("motor state on exit: ");
      Serial.println(motorState);

      Serial.print("local motor on exit: ");
      Serial.println(localMotorState);

      delay(2000);

      if (motorState == 1){

        Serial.println("");
        Serial.println("this block");
        Serial.println("");
        digitalWrite(motor, HIGH);
        globalState = 1;

        delay(1000);

      }

      else{

        Serial.println("");
        Serial.println("this block2");
        Serial.println("");
        digitalWrite(motor, LOW);
        globalState = 0;
        delay(1000);
      }
      
      Serial.println("");

      Serial.print("motor state after global: ");
      Serial.println(motorState);

      Serial.print("local motor after global: ");
      Serial.println(localMotorState);

      delay(2000);

      Serial.print("global state: ");
      Serial.println(globalState);

      delay(2000);

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
      Serial.println("Reconnecting to "+String(ssid)+" wifi network....");

      hardChanges();

    }

    Serial.println("Connected to "+String(ssid));
    syncHardChanges();

  }

  delay (dt_out);

}
