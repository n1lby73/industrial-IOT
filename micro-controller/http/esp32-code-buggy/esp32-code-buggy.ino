// void setup() {

//   Serial.begin(115200);
//   delay(100);

//   Serial.print("Attempting to connect to SSID: ");
//   Serial.println(ssid);
//   WiFi.begin(ssid, password);

//   while (WiFi.status() != WL_CONNECTED) {
//     Serial.print(".");
//     // wait 1 second for re-trying
//     delay(1000);
//   }

//   Serial.print("Connected to ");
//   Serial.println(ssid);

//   client.setCACert(test_root_ca);
//   //client.setCertificate(test_client_cert); // for client verification
//   //client.setPrivateKey(test_client_key);	// for client verification

//   Serial.println("\nStarting connection to server...");
//   if (!client.connect(server, 443))
//     Serial.println("Connection failed!");
//   else {
//     Serial.println("Connected to server!");
//     // Make a HTTP request:
//     client.println("POST https://industrialiot.onrender.com/query HTTP/1.0");
//     client.println("Host: industrialiot.onrender.com");
//     client.println("Connection: close");
//     client.println();

//     while (client.connected()) {
//       String line = client.readStringUntil('\n');
//       if (line == "\r") {
//         Serial.println("headers received");
//         break;
//       }
//     }
//     // if there are incoming bytes available
//     // from the server, read them and print them:
//     while (client.available()) {
//       char c = client.read();
//       Serial.write(c);
//     }

//     client.stop();
//   }
// }

// void loop() {
//   // do nothing
// }
/*
  Refrence:
    WiFiClient (Arduino pre-built example)
    WiFiClientBasic (Arduino pre-built exaample)
    Httpclient (Arduino pre-built example)
    
*/


    // Prepare the JSON payload
    // StaticJsonDocument<200> doc;
    // doc["param1"] = "value1";
    // doc["param2"] = "value2";

    // // Serialize the JSON document to a string
    // String payload;
    // serializeJson(doc, payload);

    // // Make a HTTP POST request with the JSON payload
    // client.println("POST /query HTTP/1.1");
    // client.println("Host: industrialiot.onrender.com");
    // client.println("Connection: close");
    // client.println("Content-Type: application/json");
    // client.print("Content-Length: ");
    // client.println(payload.length());
    // client.println();
    // client.println(payload);

    // while (client.connected()) {
    //   String line = client.readStringUntil('\n');
    //   if (line == "\r") {
    //     Serial.println("headers received");
    //     break;
    //   }
    // }

    // // If there are incoming bytes available
    // // from the server, read and print them:
    // while (client.available()) {
    //   char c = client.read();
    //   Serial.write(c);
    // }

    // client.stop();


#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <ESPping.h>
#include <WiFi.h>

int dt_out = 100; //dt_out ==> delay timer out (out denoting the end of the void loop)
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
#define password "forTheLoveOfEmbededSystem"

const char* serverID = "industrialiot.onrender.com";
const char* serverIP = "192.168.0.145"; //host subject to change always untill app is hosted
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
  doc["state"] = localMotorState;
  doc["pin"] = 5;

  String jsonString;
  serializeJson(doc, jsonString);

  String url = "http://" + String(serverID) + "/synchardchanges";

  http.begin(client, url);
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.POST(jsonString);

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

void onlineStatus(){

  String url = "http://" + String(serverID) + "/espOnline";

  http.begin(client, url);
  http.addHeader("Content-Type", "application/json");

  int httpCode = http.POST("");

  if (httpCode > 0){

  }

  http.end();
}

void setup(){ 

  pinMode(motor, OUTPUT);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.begin (115200);
  int trial = 0;
  while (WiFi.status() != WL_CONNECTED) {

     Serial.print("Connecting to "+String(ssid)+" Wifi network...");
     Serial.println(".");
     trial++;
     hardChanges();
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
  
  // Check for hardwware changes

  hardChanges();

  // Check if wifi is connected

  if (WiFi.status() == WL_CONNECTED){

    internetAccess();
    onlineStatus();
    
    String url = "http://" + String(serverID) + "/query";

    http.begin(client, url);
    http.addHeader("Content-Type", "application/json");
    int httpCode = http.POST("");

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

        localMotorState = 2;

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
