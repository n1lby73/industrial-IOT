#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <ESPping.h>
#include <WiFi.h>

int dt_out = 100; //dt_out ==> delay timer out (out denoting the end of the void loop)
int minDt = 0.5; //minDt ==> minimum timer
int wifiDt = 100;

int motor  = 26;
int motorPb = 27;
bool emergency = false;
int emergencybtn = 22;
int resetEmergencybtn = 23;
int emergencyLed = 14;
int pbStateOld;
int pbStateNew;
int localMotorState;
int motorState;
// int globalState;

#define ssid "esp8266"
#define password "forTheLoveOfEmbededSystem"

const char* serverID = "industrialiot.onrender.com";
const char* serverIP = "192.168.62.228"; //host subject to change always untill app is hosted
const int serverPort = 5000;

// Ping google.com to know if connected wifi has access to internet
const char* google = "216.58.223.238";

// Use WiFiClient and HTTPclient class to create TCP connections

IPAddress ip;
HTTPClient http;
WiFiClient client;

// Function to constantly check for changes on the hardware

void hardChanges(){

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

void syncHardChanges(){

  DynamicJsonDocument doc(200);
  doc["status"] = localMotorState;
  doc["pin"] = motor;

  String jsonString;
  serializeJson(doc, jsonString);

  String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/api/synchardchanges";

  http.begin(client, url);
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.PUT(jsonString);

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
  }

  http.end();

}

void syncEmergency(int emergencyValue){

  DynamicJsonDocument doc(200);
  doc["emergency"] = emergencyValue;

  String jsonString;
  serializeJson(doc, jsonString);

  String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/api/emergency";

  http.begin(client, url);
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.PUT(jsonString);

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
  }

  http.end();

}

void setupEmergency(){

  if (digitalRead(emergencybtn) == 1) {

      emergency = true;
      localMotorState = 0;
      digitalWrite(motor, LOW);
      digitalWrite(emergencyLed, HIGH);
      syncHardChanges();
      syncEmergency(1);

      while (digitalRead(resetEmergencybtn) != 1 && emergency) {

        Serial.println("Waiting for emergency to be reset");
        Serial.print("emergency state is: ");
        Serial.println(digitalRead(emergencybtn));
        Serial.println(" ");
        Serial.print("reset state is: ");
        Serial.println(digitalRead(resetEmergencybtn));

      }

      Serial.println(" ");
      Serial.println("emergency mode off");
      emergency = false;
      syncEmergency(0);
      digitalWrite(emergencyLed, LOW);

    }

}

void internetAccess() {

  while (!Ping.ping(google, 1)) {

    hardChanges();

    if (WiFi.status() == WL_CONNECTED){

      Serial.println(String(ssid) + " has no internet connection");
      Serial.println();
      Serial.print("Local state is ==>: ");
      Serial.println(localMotorState);
      
    }

    else{
      Serial.println("wifi disconnected");
      ESP.restart();
    }
  }


}

void setup(){ 

  pinMode(motor, OUTPUT);
  pinMode(emergencyLed, OUTPUT);
  pinMode(motorPb, INPUT);
  pinMode(emergencybtn, INPUT);
  pinMode(resetEmergencybtn, INPUT);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.begin (115200);
  int trial = 0;
  while (WiFi.status() != WL_CONNECTED) {

     Serial.print("Connecting to "+String(ssid)+" Wifi network...");
     Serial.println(".");
     trial++;
     hardChanges();
     setupEmergency();
     Serial.println(localMotorState);

     if (trial == 1000){
        Serial.println("resetting");
        ESP.restart();
      }
  }

  internetAccess();
  
  Serial.println("");
  Serial.println("WiFi connected");
}

void loop() {
  
  // when emergency is not pressed
  // Serial.println(" ");
  // Serial.print("emergency state is: ");
  // Serial.println(digitalRead(emergency));
  // Serial.println(" ");
  // Serial.print("reset state is: ");
  // Serial.println(digitalRead(resetEmergency));
  // delay(1000);

  // if (digitalRead(emergency) == 1){
  //   digitalWrite(emergencyLed, HIGH);
  //   Serial.println(digitalRead(emergencyLed));
  //   Serial.println("here");
  // }

  while ((digitalRead(emergencybtn) != 1) && (!emergency)){

    // Check for hardwware changes
    
    hardChanges();

    // Check if wifi is connected

    if (WiFi.status() == WL_CONNECTED){

      internetAccess();
      
      String url = "http://" + String(serverIP) + ":" + String(serverPort) + "/api/query";
      DynamicJsonDocument doc(200);
      doc["pin"] = motor; //pin motor is connected to....meant to be 26 but server is using 5

      String jsonString;
      serializeJson(doc, jsonString);

      http.begin(client, url);
      http.addHeader("Content-Type", "application/json");
      int httpCode = http.POST(jsonString);

      // Retrieve Json data from server

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

        // Synchronizing realtime update with local changes

        if ((motorState == 1) && (localMotorState == 3)){

          localMotorState = 2; //if the online query sends a signal of one while the local state is zero(3) change the local state to 1 

        }

        if ((motorState == 0) && (localMotorState == 2)){

          localMotorState = 3; 

        }

        // Updating and Assigning a new value to local state other than 0 and 1 o keep track of changes

        if ((localMotorState == 1) || (localMotorState == 0)){

          if (localMotorState == 1){

            syncHardChanges();
            localMotorState = 2;

          }

          else{

            syncHardChanges();
            localMotorState = 3;

          }
        }

        // Giving conditions to write the esp32 pin either high or low

        if ((motorState == 1) && (localMotorState == 2)){

          digitalWrite(motor, HIGH);

        }

        else{

          digitalWrite(motor, LOW);

        }
      }

      // Printing error code if unable to get to the server

      else{

        Serial.println("Error: " + String(httpCode));

      }

      http.end();

    }
    
    // In cases where internet is disconnected

    else{

      Serial.println("Wifi disconnected");
      delay(wifiDt);
      int trial = 0;

      while (WiFi.status() != WL_CONNECTED) {
        
      delay(wifiDt);
        Serial.println("Reconnecting to "+String(ssid)+" wifi network....");
        WiFi.disconnect();
        WiFi.begin(ssid, password);
        trial++;
        hardChanges();

        if (trial == 500){
          Serial.println("resetting");                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
          ESP.restart();
        }

      }

      internetAccess();

      Serial.println("Connected to "+String(ssid));
      syncHardChanges();

    }

    delay (dt_out);

  }

  emergency = true;
  localMotorState = 0;
  digitalWrite(motor, LOW);
  digitalWrite(emergencyLed, HIGH);
  syncHardChanges();
  syncEmergency(1);
  Serial.println(digitalRead(emergencybtn));

  while ((digitalRead(resetEmergencybtn) != 1) && (emergency)){

    Serial.println("Waiting for emergency to be reset");
    Serial.print("emergency state is: ");
    Serial.println(digitalRead(emergencybtn));
    Serial.println(" ");
    Serial.print("reset state is: ");
    Serial.println(digitalRead(resetEmergencybtn));

  }

  Serial.println(" ");
  Serial.println("outside");
  emergency = false;
  syncEmergency(0);
  digitalWrite(emergencyLed, LOW);

}