/*
  Refrence:
    WiFiClient (Arduino pre-built example)
    WiFiClientBasic (Arduino pre-built exaample)
    Httpclient (Arduino pre-built example)

*/

#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <ESPping.h>
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

#define ssid "esp8266"
#define password "forTheLoveOfEmbededSystemSs"

const char* serverIP = "192.168.137.87"; //host subject to change always untill app is hosted
const int serverPort = 3565;

// Ping google.com to know if connected wifi has access to internet
const char* google = "google.com";

// Use WiFiClient and HTTPclient class to create TCP connections

HTTPClient http;
WiFiClient client;
IPAddress ip;

// Function to constantly check for changes on the hardware

void hardChanges() {

  pbStateNew = digitalRead(motorPb);

  if ((pbStateNew == 1) && (pbStateOld == 0)) {

    if ((localMotorState == 0) || (localMotorState == 3)) {

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

// Function to send hardware changes to server

void syncHardChanges() {

  DynamicJsonDocument doc(200);
  doc["state"] = localMotorState;
  doc["pin"] = 5;

  String jsonString;
  serializeJson(doc, jsonString);

  String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/synchardchanges";

  http.begin(client, url);
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.POST(jsonString);

  if (httpCode > 0) {

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

// check if connected wifi has internet connection


void internetAccess() {

  while (!Ping.ping(google, 1)) {

    hardChanges();
    Serial.println(String(ssid) + " has no internet connection");
    Serial.println();
    Serial.print("Local state is ==>: ");
    Serial.println(localMotorState);

  }

}

void setup() {

  pinMode(motor, OUTPUT);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.begin (115200);
  int trial = 0;

  // check if wifi is connected

  while (WiFi.status() != WL_CONNECTED) {

    Serial.print("Connecting to " + String(ssid) + " Wifi network...");
    Serial.println(".");
    trial++;
    hardChanges();
    Serial.println(localMotorState);

    if (trial == 1000) {
      Serial.println("resetting");
      ESP.restart();
    }
    
  }

  internetAccess();

  Serial.println("");
  Serial.println("WiFi connected with internet access");

}

void loop() {

  // Check for hardwware changes

  hardChanges();

  // Check if wifi is connected

  if (WiFi.status() == WL_CONNECTED) {

    internetAccess();

    String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/query";

    http.begin(client, url);

    int httpCode = http.POST("");

    // Retrieve Json data from server

    if (httpCode > 0) {

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

      // Synchronizing realtime update with local changes

      if ((motorState == 1) && (localMotorState == 3)) {

        localMotorState = 2;

      }

      if ((motorState == 0) && (localMotorState == 2)) {

        localMotorState = 3;

      }

      // Updating and Assigning a new value to local state other than 0 and 1 o keep track of changes

      if ((localMotorState == 1) || (localMotorState == 0)) {

        if (localMotorState == 1) {

          syncHardChanges();
          localMotorState = 2;

        }

        else {

          syncHardChanges();
          localMotorState = 3;

        }
      }

      // Giving conditions to write the esp32 pin either high or low

      if ((motorState == 1) && (localMotorState == 2)) {

        digitalWrite(motor, HIGH);

      }

      else {

        digitalWrite(motor, LOW);

      }
    }

    // Printing error code if unable to get to the server

    else {

      Serial.println("Error: " + String(httpCode));

    }

    http.end();

  }

  // In cases where internet is disconnected

  else {

    Serial.println("Wifi disconnected");
    delay(wifiDt);
    int trial = 0;

    while (WiFi.status() != WL_CONNECTED) {

      delay(wifiDt);
      Serial.println("Reconnecting to " + String(ssid) + " wifi network....");
      WiFi.disconnect();
      WiFi.begin(ssid, password);
      trial++;
      hardChanges();

      if (trial == 500) {
        Serial.println("resetting");
        ESP.restart();
      }

    }

    Serial.println("Connected to " + String(ssid));
    syncHardChanges();

  }

  delay (dt_out);

}