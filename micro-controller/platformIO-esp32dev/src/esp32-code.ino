/*
  Refrence:
    WiFiClient (Arduino pre-built example)
    WiFiClientBasic (Arduino pre-built exaample)
    Httpclient (Arduino pre-built example)
    WiFiClientSecure (Arduino pre-built exaample)
    
*/

#include <Arduino.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>
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

const char* ssid = "esp8266";
const char* password = "forTheLoveOfEmbededSystem";

const int port = 443;
const char*  server = "https://industrialiot.onrender.com";  // Server URL

// Ping google.com to know if connected wifi has access to internet
const char* google = "216.58.223.238";

// Server certificate
const char* test_root_ca = 
"-----BEGIN CERTIFICATE-----\n" \
"MIIDdzCCAl+gAwIBAgIEAgAAuTANBgkqhkiG9w0BAQUFADBaMQswCQYDVQQGEwJJ\n" \
"RTESMBAGA1UEChMJQmFsdGltb3JlMRMwEQYDVQQLEwpDeWJlclRydXN0MSIwIAYD\n" \
"VQQDExlCYWx0aW1vcmUgQ3liZXJUcnVzdCBSb290MB4XDTAwMDUxMjE4NDYwMFoX\n" \
"DTI1MDUxMjIzNTkwMFowWjELMAkGA1UEBhMCSUUxEjAQBgNVBAoTCUJhbHRpbW9y\n" \
"ZTETMBEGA1UECxMKQ3liZXJUcnVzdDEiMCAGA1UEAxMZQmFsdGltb3JlIEN5YmVy\n" \
"VHJ1c3QgUm9vdDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKMEuyKr\n" \
"mD1X6CZymrV51Cni4eiVgLGw41uOKymaZN+hXe2wCQVt2yguzmKiYv60iNoS6zjr\n" \
"IZ3AQSsBUnuId9Mcj8e6uYi1agnnc+gRQKfRzMpijS3ljwumUNKoUMMo6vWrJYeK\n" \
"mpYcqWe4PwzV9/lSEy/CG9VwcPCPwBLKBsua4dnKM3p31vjsufFoREJIE9LAwqSu\n" \
"XmD+tqYF/LTdB1kC1FkYmGP1pWPgkAx9XbIGevOF6uvUA65ehD5f/xXtabz5OTZy\n" \
"dc93Uk3zyZAsuT3lySNTPx8kmCFcB5kpvcY67Oduhjprl3RjM71oGDHweI12v/ye\n" \
"jl0qhqdNkNwnGjkCAwEAAaNFMEMwHQYDVR0OBBYEFOWdWTCCR1jMrPoIVDaGezq1\n" \
"BE3wMBIGA1UdEwEB/wQIMAYBAf8CAQMwDgYDVR0PAQH/BAQDAgEGMA0GCSqGSIb3\n" \
"DQEBBQUAA4IBAQCFDF2O5G9RaEIFoN27TyclhAO992T9Ldcw46QQF+vaKSm2eT92\n" \
"9hkTI7gQCvlYpNRhcL0EYWoSihfVCr3FvDB81ukMJY2GQE/szKN+OMY3EU/t3Wgx\n" \
"jkzSswF07r51XgdIGn9w/xZchMB5hbgF/X++ZRGjD8ACtPhSNzkE1akxehi/oCr0\n" \
"Epn3o0WC4zxe9Z2etciefC7IpJ5OCBRLbf1wbWsaY71k5h+3zvDyny67G7fyUIhz\n" \
"ksLi4xaNmjICq44Y3ekQEe5+NauQrz4wlHrQMz2nZQ/1/I6eYs9HRCwBXbsdtTLS\n" \
"R9I4LtD+gdwyah617jzV/OeBHRnDJELqYzmp\n" \
"-----END CERTIFICATE-----\n";

IPAddress ip;
WiFiClientSecure client;

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
  Serial.println ("jsdkanjksdf");
  DynamicJsonDocument doc(200);
  doc["state"] = localMotorState;
  doc["pin"] = 5;

  String jsonString;
  serializeJson(doc, jsonString);
  client.setCACert(test_root_ca);
  if (client.connect(server, port)){

    client.print("POST /synchardchanges HTTP/1.1");
    client.print("Host: industrialiot.onrender.com");
    client.print("Content-Type: application/json");
    client.print("Content-Length: " + String(jsonString.length()));
    client.print("Connection: close");
    client.print("");
    client.print(jsonString);
    
    // client.print();
/*
  Refrence:
    WiFiClient (Arduino pre-built example)
    WiFiClientBasic (Arduino pre-built exaample)
    Httpclient (Arduino pre-built example)
    WiFiClientSecure (Arduino pre-built exaample)
    
*/

#include <Arduino.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>
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

const char* ssid = "esp8266";
const char* password = "forTheLoveOfEmbededSystem";

const int port = 443;
const char*  server = "https://industrialiot.onrender.com";  // Server URL

// Ping google.com to know if connected wifi has access to internet
const char* google = "216.58.223.238";

// Server certificate
const char* test_root_ca = 
"-----BEGIN CERTIFICATE-----\n" \
"MIIDdzCCAl+gAwIBAgIEAgAAuTANBgkqhkiG9w0BAQUFADBaMQswCQYDVQQGEwJJ\n" \
"RTESMBAGA1UEChMJQmFsdGltb3JlMRMwEQYDVQQLEwpDeWJlclRydXN0MSIwIAYD\n" \
"VQQDExlCYWx0aW1vcmUgQ3liZXJUcnVzdCBSb290MB4XDTAwMDUxMjE4NDYwMFoX\n" \
"DTI1MDUxMjIzNTkwMFowWjELMAkGA1UEBhMCSUUxEjAQBgNVBAoTCUJhbHRpbW9y\n" \
"ZTETMBEGA1UECxMKQ3liZXJUcnVzdDEiMCAGA1UEAxMZQmFsdGltb3JlIEN5YmVy\n" \
"VHJ1c3QgUm9vdDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKMEuyKr\n" \
"mD1X6CZymrV51Cni4eiVgLGw41uOKymaZN+hXe2wCQVt2yguzmKiYv60iNoS6zjr\n" \
"IZ3AQSsBUnuId9Mcj8e6uYi1agnnc+gRQKfRzMpijS3ljwumUNKoUMMo6vWrJYeK\n" \
"mpYcqWe4PwzV9/lSEy/CG9VwcPCPwBLKBsua4dnKM3p31vjsufFoREJIE9LAwqSu\n" \
"XmD+tqYF/LTdB1kC1FkYmGP1pWPgkAx9XbIGevOF6uvUA65ehD5f/xXtabz5OTZy\n" \
"dc93Uk3zyZAsuT3lySNTPx8kmCFcB5kpvcY67Oduhjprl3RjM71oGDHweI12v/ye\n" \
"jl0qhqdNkNwnGjkCAwEAAaNFMEMwHQYDVR0OBBYEFOWdWTCCR1jMrPoIVDaGezq1\n" \
"BE3wMBIGA1UdEwEB/wQIMAYBAf8CAQMwDgYDVR0PAQH/BAQDAgEGMA0GCSqGSIb3\n" \
"DQEBBQUAA4IBAQCFDF2O5G9RaEIFoN27TyclhAO992T9Ldcw46QQF+vaKSm2eT92\n" \
"9hkTI7gQCvlYpNRhcL0EYWoSihfVCr3FvDB81ukMJY2GQE/szKN+OMY3EU/t3Wgx\n" \
"jkzSswF07r51XgdIGn9w/xZchMB5hbgF/X++ZRGjD8ACtPhSNzkE1akxehi/oCr0\n" \
"Epn3o0WC4zxe9Z2etciefC7IpJ5OCBRLbf1wbWsaY71k5h+3zvDyny67G7fyUIhz\n" \
"ksLi4xaNmjICq44Y3ekQEe5+NauQrz4wlHrQMz2nZQ/1/I6eYs9HRCwBXbsdtTLS\n" \
"R9I4LtD+gdwyah617jzV/OeBHRnDJELqYzmp\n" \
"-----END CERTIFICATE-----\n";

IPAddress ip;
WiFiClientSecure client;

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
  Serial.println ("jsdkanjksdf");
  DynamicJsonDocument doc(200);
  doc["state"] = localMotorState;
  doc["pin"] = 5;

  String jsonString;
  serializeJson(doc, jsonString);
  client.setCACert(test_root_ca);
  if (client.connect(server, port)){

    client.print("POST /synchardchanges HTTP/1.1");
    client.print("Host: industrialiot.onrender.com");
    client.print("Content-Type: application/json");
    client.print("Content-Length: " + String(jsonString.length()));
    client.print("Connection: close");
    client.print();
    client.print(jsonString);
    
    // client.print();

    // Wait for the server's response and read the response data
    while (client.connected() && !client.available()) {

      delay(100);

    }

    while (client.available()) {
      
      String payload;
      char c = client.read();
      payload += c;

      DynamicJsonDocument doc(500);
      DeserializationError error = deserializeJson(doc, payload);

      if (error) {

        Serial.println("Deserialization failed: " + String(error.c_str()));
        return;

      }

      motorState = doc["success"];

      Serial.println(motorState);
      Serial.println ("yyyyyyyyyyyyyyyyyyyyyyyyyyyyy");

    }

    client.stop();
    Serial.println ("byeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee");
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

void onlineStatus(){

  if (!client.connect(server, port)){

    Serial.println("Connection failed!");

  }

  else {

    Serial.println("Connected to server!");

    // Make a HTTP request:

    client.println("POST /espOnline HTTP/1.0");
    client.println("Host: industrialiot.onrender.com");
    client.println("Connection: close");
    client.println();

    while (client.connected()) {

      String line = client.readStringUntil('\n');

      if (line == "\r") {

        Serial.println("headers received");
        break;

      }
    }
    client.stop();
  }
}

void setup() {

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
  
  Serial.println("");
  Serial.println("WiFi connected");

  internetAccess();

  client.setCACert(test_root_ca);

}

void loop() {

  // Check for hardwware changes

  hardChanges();

  // Check if wifi is connected

  if (WiFi.status() == WL_CONNECTED){

    hardChanges();
    internetAccess();
    onlineStatus();
    syncHardChanges();
  
    // String url = "http://" + String(serverID) + "/query";

    // http.begin(client, url);
    // http.addHeader("Content-Type", "application/json");
    // int httpCode = http.POST("");

  //   if (!client.connect(server, 443)){

  //     Serial.println("Connection failed!");
    
  //   }

  //   else {
    
  //   Serial.println("Connected to server!");
  //   // Make a HTTP request:
  //   client.println("POST /query HTTP/1.0");
  //   client.println("Host: industrialiot.onrender.com");
  //   client.println("Connection: close");
  //   client.println();

  //   while (client.connected()) {
  //     String line = client.readStringUntil('\n');
  //     if (line == "\r") {
  //       Serial.println("headers received");
  //       break;
  //     }
  //   }
  //   // if there are incoming bytes available
  //   // from the server, read them and print them:
  //   while (client.available()) {
  //     char c = client.read();
  //     Serial.write(c);
  //   }

  //   client.stop();
  //   }
  //   // Retrieve Json data from server

  //   if (httpCode > 0){
  //     String payload = http.getString();
  //     int json = payload.indexOf("{");
  //     String jsonData = payload.substring(json);
      
  //     DynamicJsonDocument doc(200);
  //     DeserializationError error = deserializeJson(doc, jsonData);
      
  //     if (error) {

  //       Serial.println("Deserialization failed: " + String(error.c_str()));
        
  //       return;

  //     }
      
  //     motorState = doc["success"];

  //     // Synchronizing realtime update with local changes

  //     if ((motorState == 1) && (localMotorState == 3)){

  //       localMotorState = 2;

  //     }

  //     if ((motorState == 0) && (localMotorState == 2)){

  //       localMotorState = 3;

  //     }

  //     // Updating and Assigning a new value to local state other than 0 and 1 o keep track of changes

  //     if ((localMotorState == 1) || (localMotorState == 0)){

  //       if (localMotorState == 1){

  //         syncHardChanges();
  //         localMotorState = 2;

  //       }

  //       else{

  //         syncHardChanges();
  //         localMotorState = 3;

  //       }
  //     }

  //     // Giving conditions to write the esp32 pin either high or low

  //     if ((motorState == 1) && (localMotorState == 2)){

  //       digitalWrite(motor, HIGH);

  //     }

  //     else{

  //       digitalWrite(motor, LOW);

  //     }
  //   }

  //   // Printing error code if unable to get to the server

  //   else{

  //     Serial.println("Error: " + String(httpCode));

  //   }

  //   http.end();

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

    // Wait for the server's response and read the response data
    while (client.connected() && !client.available()) {

      delay(100);

    }

    while (client.available()) {
      
      String payload;
      char c = client.read();
      payload += c;

      DynamicJsonDocument doc(500);
      DeserializationError error = deserializeJson(doc, payload);

      if (error) {

        Serial.println("Deserialization failed: " + String(error.c_str()));
        return;

      }

      motorState = doc["success"];

      Serial.println(motorState);
      Serial.println ("yyyyyyyyyyyyyyyyyyyyyyyyyyyyy");

    }

    client.stop();
    Serial.println ("byeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee");
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

void onlineStatus(){

  if (!client.connect(server, port)){

    Serial.println("Connection failed!");

  }

  else {

    Serial.println("Connected to server!");

    // Make a HTTP request:

    client.println("POST /espOnline HTTP/1.0");
    client.println("Host: industrialiot.onrender.com");
    client.println("Connection: close");
    client.println();

    while (client.connected()) {

      String line = client.readStringUntil('\n');

      if (line == "\r") {

        Serial.println("headers received");
        break;

      }
    }
    client.stop();
  }
}

void setup() {

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
  
  Serial.println("");
  Serial.println("WiFi connected");

  internetAccess();

  client.setCACert(test_root_ca);

}

void loop() {

  // Check for hardwware changes

  hardChanges();

  // Check if wifi is connected

  if (WiFi.status() == WL_CONNECTED){

    hardChanges();
    internetAccess();
    onlineStatus();
    syncHardChanges();
  
    // String url = "http://" + String(serverID) + "/query";

    // http.begin(client, url);
    // http.addHeader("Content-Type", "application/json");
    // int httpCode = http.POST("");

  //   if (!client.connect(server, 443)){

  //     Serial.println("Connection failed!");
    
  //   }

  //   else {
    
  //   Serial.println("Connected to server!");
  //   // Make a HTTP request:
  //   client.println("POST /query HTTP/1.0");
  //   client.println("Host: industrialiot.onrender.com");
  //   client.println("Connection: close");
  //   client.println();

  //   while (client.connected()) {
  //     String line = client.readStringUntil('\n');
  //     if (line == "\r") {
  //       Serial.println("headers received");
  //       break;
  //     }
  //   }
  //   // if there are incoming bytes available
  //   // from the server, read them and print them:
  //   while (client.available()) {
  //     char c = client.read();
  //     Serial.write(c);
  //   }

  //   client.stop();
  //   }
  //   // Retrieve Json data from server

  //   if (httpCode > 0){
  //     String payload = http.getString();
  //     int json = payload.indexOf("{");
  //     String jsonData = payload.substring(json);
      
  //     DynamicJsonDocument doc(200);
  //     DeserializationError error = deserializeJson(doc, jsonData);
      
  //     if (error) {

  //       Serial.println("Deserialization failed: " + String(error.c_str()));
        
  //       return;

  //     }
      
  //     motorState = doc["success"];

  //     // Synchronizing realtime update with local changes

  //     if ((motorState == 1) && (localMotorState == 3)){

  //       localMotorState = 2;

  //     }

  //     if ((motorState == 0) && (localMotorState == 2)){

  //       localMotorState = 3;

  //     }

  //     // Updating and Assigning a new value to local state other than 0 and 1 o keep track of changes

  //     if ((localMotorState == 1) || (localMotorState == 0)){

  //       if (localMotorState == 1){

  //         syncHardChanges();
  //         localMotorState = 2;

  //       }

  //       else{

  //         syncHardChanges();
  //         localMotorState = 3;

  //       }
  //     }

  //     // Giving conditions to write the esp32 pin either high or low

  //     if ((motorState == 1) && (localMotorState == 2)){

  //       digitalWrite(motor, HIGH);

  //     }

  //     else{

  //       digitalWrite(motor, LOW);

  //     }
  //   }

  //   // Printing error code if unable to get to the server

  //   else{

  //     Serial.println("Error: " + String(httpCode));

  //   }

  //   http.end();

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
