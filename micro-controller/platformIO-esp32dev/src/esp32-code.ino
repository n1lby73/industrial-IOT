// /*
//   Refrence:
//     WiFiClient (Arduino pre-built example)
//     WiFiClientSecure (Arduino pre-built example)
//     WiFiClientBasic (Arduino pre-built exaample)
//     Httpclient (Arduino pre-built example)
    
// */

// #include <Arduino.h>

// #include <WiFi.h>
// #include <ESPping.h>
// #include <ArduinoJson.h>
// #include <WiFiClientSecure.ha>

// int dt_out = 100; //dt_out ==> delay timer out (out denoting the end of the void loop)
// int minDt = 0.5; //minDt ==> minimum timer
// int wifiDt = 100;

// int motor  = 26;
// int motorPb = 27;
// int pbStateOld;
// int pbStateNew;
// int localMotorState;
// int motorState;
// int globalState;

// const char* ssid = "esp8266";
// const char* password = "forTheLoveOfEmbededSystem";

// const char*  server = "https://industrialiot.onrender.com";  // Server URL

// // const char* host = "industrialiot.onrender.com";

// // Ping google.com to know if connected wifi has access to internet
// const char* google = "216.58.223.238";

// const char* test_root_ca = 
// "-----BEGIN CERTIFICATE-----\n" \
// "MIIDdzCCAl+gAwIBAgIEAgAAuTANBgkqhkiG9w0BAQUFADBaMQswCQYDVQQGEwJJ\n" \
// "RTESMBAGA1UEChMJQmFsdGltb3JlMRMwEQYDVQQLEwpDeWJlclRydXN0MSIwIAYD\n" \
// "VQQDExlCYWx0aW1vcmUgQ3liZXJUcnVzdCBSb290MB4XDTAwMDUxMjE4NDYwMFoX\n" \
// "DTI1MDUxMjIzNTkwMFowWjELMAkGA1UEBhMCSUUxEjAQBgNVBAoTCUJhbHRpbW9y\n" \
// "ZTETMBEGA1UECxMKQ3liZXJUcnVzdDEiMCAGA1UEAxMZQmFsdGltb3JlIEN5YmVy\n" \
// "VHJ1c3QgUm9vdDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAKMEuyKr\n" \
// "mD1X6CZymrV51Cni4eiVgLGw41uOKymaZN+hXe2wCQVt2yguzmKiYv60iNoS6zjr\n" \
// "IZ3AQSsBUnuId9Mcj8e6uYi1agnnc+gRQKfRzMpijS3ljwumUNKoUMMo6vWrJYeK\n" \
// "mpYcqWe4PwzV9/lSEy/CG9VwcPCPwBLKBsua4dnKM3p31vjsufFoREJIE9LAwqSu\n" \
// "XmD+tqYF/LTdB1kC1FkYmGP1pWPgkAx9XbIGevOF6uvUA65ehD5f/xXtabz5OTZy\n" \
// "dc93Uk3zyZAsuT3lySNTPx8kmCFcB5kpvcY67Oduhjprl3RjM71oGDHweI12v/ye\n" \
// "jl0qhqdNkNwnGjkCAwEAAaNFMEMwHQYDVR0OBBYEFOWdWTCCR1jMrPoIVDaGezq1\n" \
// "BE3wMBIGA1UdEwEB/wQIMAYBAf8CAQMwDgYDVR0PAQH/BAQDAgEGMA0GCSqGSIb3\n" \
// "DQEBBQUAA4IBAQCFDF2O5G9RaEIFoN27TyclhAO992T9Ldcw46QQF+vaKSm2eT92\n" \
// "9hkTI7gQCvlYpNRhcL0EYWoSihfVCr3FvDB81ukMJY2GQE/szKN+OMY3EU/t3Wgx\n" \
// "jkzSswF07r51XgdIGn9w/xZchMB5hbgF/X++ZRGjD8ACtPhSNzkE1akxehi/oCr0\n" \
// "Epn3o0WC4zxe9Z2etciefC7IpJ5OCBRLbf1wbWsaY71k5h+3zvDyny67G7fyUIhz\n" \
// "ksLi4xaNmjICq44Y3ekQEe5+NauQrz4wlHrQMz2nZQ/1/I6eYs9HRCwBXbsdtTLS\n" \
// "R9I4LtD+gdwyah617jzV/OeBHRnDJELqYzmp\n" \
// "-----END CERTIFICATE-----\n";

// IPAddress ip;
// WiFiClientSecure client;

// // Function to constantly check for changes on the hardware

// void hardChanges(){

//   pbStateNew = digitalRead(motorPb);

//   if ((pbStateNew == 1) && (pbStateOld == 0)) {

//     if ((localMotorState == 0) || (localMotorState == 3)) {

//       digitalWrite(motor, HIGH);
//       localMotorState = 1;

//     }

//     else {

//       digitalWrite(motor, LOW);
//       localMotorState = 0;

//     }
//   }

//   pbStateOld = pbStateNew;

// }

// // Function to send hardware changes to server

// void syncHardChanges(){

//   DynamicJsonDocument doc(200);
//   doc["state"] = localMotorState;
//   doc["pin"] = 5;

//   String jsonString;
//   serializeJson(doc, jsonString);

//   client.println("POST /synchardchanges HTTP/1.1");
//   client.println("Host: industrialiot.onrender.com");
//   client.println("Connection: close");
//   client.println("Content-Type: application/json");
//   client.print("Content-Length: ");
//   client.println(jsonString.length());
//   client.println();
//   client.println(jsonString);

//   while (client.connected()) {
//     String line = client.readStringUntil('\n');
//     if (line == "\r") {
//       Serial.println("headers received");
//       break;
//     }
//   }

//   while (client.available()) {

//     char c = client.read();
//     Serial.write(c);

//   }

//   client.stop();

// }

// void internetAccess() {

//   while (!Ping.ping(google, 1)) {

//     hardChanges();

//     if (WiFi.status() == WL_CONNECTED){

//       Serial.println(String(ssid) + " has no internet connection");
//       Serial.println();
//       Serial.print("Local state is ==>: ");
//       Serial.println(localMotorState);
      
//     }

//     else{
//       Serial.println("wifi disconnected");
//       ESP.restart();
//     }
//   }


// }

// // void onlineStatus(){

// //   String url = "http://" + String(serverID) + "/espOnline";

// //   http.begin(client, url);
// //   http.addHeader("Content-Type", "application/json");

// //   int httpCode = http.POST("");

// //   if (httpCode > 0){

// //   }

// //   http.end();
// // }

// void setup(){ 

//   pinMode(motor, OUTPUT);

//   WiFi.mode(WIFI_STA);
//   WiFi.begin(ssid, password);

//   Serial.begin (115200);
//   int trial = 0;
//   while (WiFi.status() != WL_CONNECTED) {

//      Serial.print("Connecting to "+String(ssid)+" Wifi network...");
//      Serial.println(".");
//      trial++;
//      hardChanges();
//      Serial.println(localMotorState);

//      if (trial == 1000){
//         Serial.println("resetting");
//         ESP.restart();
//       }
//   }

//   // internetAccess();
  
//   Serial.println("");
//   Serial.println("WiFi connected");

//   client.setCACert(test_root_ca);

//   DynamicJsonDocument doc(200);
//   doc["state"] = localMotorState;
//   doc["pin"] = 5;

//   String jsonString;
//   serializeJson(doc, jsonString);

//   client.println("POST /synchardchanges HTTP/1.1");
//   client.println("Host: industrialiot.onrender.com");
//   client.println("Connection: close");
//   client.println("Content-Type: application/json");
//   client.print("Content-Length: ");
//   client.println(jsonString.length());
//   client.println();
//   client.println(jsonString);

//   while (client.connected()) {
//     String line = client.readStringUntil('\n');
//     if (line == "\r") {
//       Serial.println("headers received");
//       break;
//     }
//   }

//   while (client.available()) {

//     char c = client.read();
//     Serial.write(c);

//   }

//   client.stop();
// }

// // void loop() {
  
// //   // Check for hardwware changes

// //   hardChanges();

// //   // Check if wifi is connected

// //   if (WiFi.status() == WL_CONNECTED){

// //     internetAccess();
// //     onlineStatus();
    
// //     String url = "http://" + String(serverID) + "/query";

// //     http.begin(client, url);
// //     http.addHeader("Content-Type", "application/json");
// //     int httpCode = http.POST("");

// //     // Retrieve Json data from server

// //     if (httpCode > 0){
// //       String payload = http.getString();
// //       int json = payload.indexOf("{");
// //       String jsonData = payload.substring(json);
      
// //       DynamicJsonDocument doc(200);
// //       DeserializationError error = deserializeJson(doc, jsonData);
      
// //       if (error) {

// //         Serial.println("Deserialization failed: " + String(error.c_str()));
        
// //         return;

// //       }
      
// //       motorState = doc["success"];

// //       // Synchronizing realtime update with local changes

// //       if ((motorState == 1) && (localMotorState == 3)){

// //         localMotorState = 2;

// //       }

// //       if ((motorState == 0) && (localMotorState == 2)){

// //         localMotorState = 3;

// //       }

// //       // Updating and Assigning a new value to local state other than 0 and 1 o keep track of changes

// //       if ((localMotorState == 1) || (localMotorState == 0)){

// //         if (localMotorState == 1){

// //           syncHardChanges();
// //           localMotorState = 2;

// //         }

// //         else{

// //           syncHardChanges();
// //           localMotorState = 3;

// //         }
// //       }

// //       // Giving conditions to write the esp32 pin either high or low

// //       if ((motorState == 1) && (localMotorState == 2)){

// //         digitalWrite(motor, HIGH);

// //       }

// //       else{

// //         digitalWrite(motor, LOW);

// //       }
// //     }

// //     // Printing error code if unable to get to the server

// //     else{

// //       Serial.println("Error: " + String(httpCode));

// //     }

// //     http.end();

// //   }
  
// //   // In cases where internet is disconnected

// //   else{

// //     Serial.println("Wifi disconnected");
// //     delay(wifiDt);
// //     int trial = 0;

// //     while (WiFi.status() != WL_CONNECTED) {
      
// //      delay(wifiDt);
// //       Serial.println("Reconnecting to "+String(ssid)+" wifi network....");
// //       WiFi.disconnect();
// //       WiFi.begin(ssid, password);
// //       trial++;
// //       hardChanges();

// //       if (trial == 500){
// //         Serial.println("resetting");
// //         ESP.restart();
// //       }

// //     }

// //     internetAccess();

// //     Serial.println("Connected to "+String(ssid));
// //     syncHardChanges();

// //   }

// //   delay (dt_out);

// // }
// // void setup() {

// //   Serial.begin(115200);
// //   delay(100);

// //   Serial.print("Attempting to connect to SSID: ");
// //   Serial.println(ssid);
// //   WiFi.begin(ssid, password);

// //   while (WiFi.status() != WL_CONNECTED) {
// //     Serial.print(".");
// //     // wait 1 second for re-trying
// //     delay(1000);
// //   }

// //   Serial.print("Connected to ");
// //   Serial.println(ssid);

// //   client.setCACert(test_root_ca);
// //   //client.setCertificate(test_client_cert); // for client verification
// //   //client.setPrivateKey(test_client_key);	// for client verification

// //   Serial.println("\nStarting connection to server...");
// //   if (!client.connect(server, 443))
// //     Serial.println("Connection failed!");
// //   else {
// //     Serial.println("Connected to server!");
// //     // Make a HTTP request:
// //     client.println("POST https://industrialiot.onrender.com/query HTTP/1.0");
// //     client.println("Host: industrialiot.onrender.com");
// //     client.println("Connection: close");
// //     client.println();

// //     while (client.connected()) {
// //       String line = client.readStringUntil('\n');
// //       if (line == "\r") {
// //         Serial.println("headers received");
// //         break;
// //       }
// //     }
// //     // if there are incoming bytes available
// //     // from the server, read them and print them:
// //     while (client.available()) {
// //       char c = client.read();
// //       Serial.write(c);
// //     }

// //     client.stop();
// //   }
// // }

// void loop() {
//   // do nothing
// }

// #include <WiFi.h>
// #include <WiFiClientSecure.h>

// const char* ssid = "esp8266";
// const char* password = "forTheLoveOfEmbededSystem";

// const char* host = "https://industrialiot.onrender.com";
// const int httpsPort = 443;

// // Root certificate for the server
// const char* rootCACertificate = "-----BEGIN CERTIFICATE-----\n"
// "MIIFNDCCBNqgAwIBAgIQCC9vXhMOqjhjh/fFfICYmTAKBggqhkjOPQQDAjBKMQsw\n"\
// "CQYDVQQGEwJVUzEZMBcGA1UEChMQQ2xvdWRmbGFyZSwgSW5jLjEgMB4GA1UEAxMX\n"\
// "Q2xvdWRmbGFyZSBJbmMgRUNDIENBLTMwHhcNMjMwNDI1MDAwMDAwWhcNMjQwNDIz\n"\
// "MjM1OTU5WjB1MQswCQYDVQQGEwJVUzETMBEGA1UECBMKQ2FsaWZvcm5pYTEWMBQG\n"\
// "A1UEBxMNU2FuIEZyYW5jaXNjbzEZMBcGA1UEChMQQ2xvdWRmbGFyZSwgSW5jLjEe\n"\
// "MBwGA1UEAxMVc25pLmNsb3VkZmxhcmVzc2wuY29tMFkwEwYHKoZIzj0CAQYIKoZI\n"\
// "zj0DAQcDQgAESe3PljFfsfWY/UJwLvX39Es+PH0EnxrZ7LHXgwMpPmHuZnlWRW/j\n"\
// "VVGdGnrc68bhtmIaSqyzTPvmGStQpoCgxKOCA3UwggNxMB8GA1UdIwQYMBaAFKXO\n"\
// "N+rrsHUOlGeItEX62SQQh5YfMB0GA1UdDgQWBBQQqEe2OJuOgKxBzIYtfUWM0gbU\n"\
// "iDA8BgNVHREENTAzghVzbmkuY2xvdWRmbGFyZXNzbC5jb22CGmluZHVzdHJpYWxp\n"\
// "b3Qub25yZW5kZXIuY29tMA4GA1UdDwEB/wQEAwIHgDAdBgNVHSUEFjAUBggrBgEF\n"\
// "BQcDAQYIKwYBBQUHAwIwewYDVR0fBHQwcjA3oDWgM4YxaHR0cDovL2NybDMuZGln\n"\
// "aWNlcnQuY29tL0Nsb3VkZmxhcmVJbmNFQ0NDQS0zLmNybDA3oDWgM4YxaHR0cDov\n"\
// "L2NybDQuZGlnaWNlcnQuY29tL0Nsb3VkZmxhcmVJbmNFQ0NDQS0zLmNybDA+BgNV\n"\
// "HSAENzA1MDMGBmeBDAECAjApMCcGCCsGAQUFBwIBFhtodHRwOi8vd3d3LmRpZ2lj\n"\
// "ZXJ0LmNvbS9DUFMwdgYIKwYBBQUHAQEEajBoMCQGCCsGAQUFBzABhhhodHRwOi8v\n"\
// "b2NzcC5kaWdpY2VydC5jb20wQAYIKwYBBQUHMAKGNGh0dHA6Ly9jYWNlcnRzLmRp\n"\
// "Z2ljZXJ0LmNvbS9DbG91ZGZsYXJlSW5jRUNDQ0EtMy5jcnQwDAYDVR0TAQH/BAIw\n"\
// "ADCCAX0GCisGAQQB1nkCBAIEggFtBIIBaQFnAHUA7s3QZNXbGs7FXLedtM0TojKH\n"\
// "Rny87N7DUUhZRnEftZsAAAGHula9PgAABAMARjBEAiAo1LKjZ7GCS4NtrQfPIBs7\n"\
// "6Yl8IQoj2l3GrVjpZJeXyQIgVygiIxo/bKaP2cBPjNDDZ7SNRGNb8sxK/+jVixbq\n"\
// "tEsAdgBz2Z6JG0yWeKAgfUed5rLGHNBRXnEZKoxrgBB6wXdytQAAAYe6Vr13AAAE\n"\
// "AwBHMEUCIQCPtn6ZfB3otXJE96wo77OO0iDjDlBmptaFk3k3OzcC/AIgQvlAeNSV\n"\
// "dmUu5h1mrBG3gLhftRL0xjy53P+Bwxo0tcQAdgBIsONr2qZHNA/lagL6nTDrHFIB\n"\
// "y1bdLIHZu7+rOdiEcwAAAYe6Vr1eAAAEAwBHMEUCIFmI7nPYuSuGHakZvDf3sn5b\n"\
// "ZVa25g1MesfH9GlwAOdIAiEA5WzCFrFe2pB8voAA/gpTwgXZ0WsnJMFBxIU/kjRP\n"\
// "/wswCgYIKoZIzj0EAwIDSAAwRQIhANHGjpotdE3x+Roghod99sY8dKOHUuwrAI5U\n"\
// "kyuiFa7MAiA/pxvobn/sikKd/YtnN6XQe+llfZskXNxVwXQWjodHAw==\n"\
// "-----END CERTIFICATE-----";

// void setup() {
//   Serial.begin(115200);
//   // Connect to Wi-Fi
//   WiFi.begin(ssid, password);
//   while (WiFi.status() != WL_CONNECTED) {
//     delay(1000);
//     Serial.println("Connecting to WiFi...");
//   }
//   Serial.println("Connected to WiFi");

//   // Create a WiFiClientSecure object
//   WiFiClientSecure client;

//   // Set the root certificate
//   client.setCACert(rootCACertificate);

//   // Connect to the server
//   if (!client.connect(host, httpsPort)) {
//     Serial.println("Connection failed!");
//     return;
//   }

//   // Make an HTTP GET request
//   client.print(String("GET /query HTTP/1.1\r\n") +
//                "Host: " + host + "\r\n" +
//                "Connection: close\r\n\r\n");

//   Serial.println("Request sent!");

//   // Wait for the response
//   while (client.connected()) {
//     String line = client.readStringUntil('\n');
//     Serial.println(line);
//   }

//   Serial.println("Response received!");

//   // Disconnect from the server
//   client.stop();
// }

// void loop() {
//   // Empty loop
// }
/*
  Wifi secure connection example for ESP32
  Running on TLS 1.2 using mbedTLS
  Suporting the following chipersuites:
  "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384","TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384","TLS_DHE_RSA_WITH_AES_256_GCM_SHA384","TLS_ECDHE_ECDSA_WITH_AES_256_CCM","TLS_DHE_RSA_WITH_AES_256_CCM","TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384","TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384","TLS_DHE_RSA_WITH_AES_256_CBC_SHA256","TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA","TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA","TLS_DHE_RSA_WITH_AES_256_CBC_SHA","TLS_ECDHE_ECDSA_WITH_AES_256_CCM_8","TLS_DHE_RSA_WITH_AES_256_CCM_8","TLS_ECDHE_ECDSA_WITH_CAMELLIA_256_GCM_SHA384","TLS_ECDHE_RSA_WITH_CAMELLIA_256_GCM_SHA384","TLS_DHE_RSA_WITH_CAMELLIA_256_GCM_SHA384","TLS_ECDHE_ECDSA_WITH_CAMELLIA_256_CBC_SHA384","TLS_ECDHE_RSA_WITH_CAMELLIA_256_CBC_SHA384","TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA256","TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA","TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256","TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256","TLS_DHE_RSA_WITH_AES_128_GCM_SHA256","TLS_ECDHE_ECDSA_WITH_AES_128_CCM","TLS_DHE_RSA_WITH_AES_128_CCM","TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256","TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256","TLS_DHE_RSA_WITH_AES_128_CBC_SHA256","TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA","TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA","TLS_DHE_RSA_WITH_AES_128_CBC_SHA","TLS_ECDHE_ECDSA_WITH_AES_128_CCM_8","TLS_DHE_RSA_WITH_AES_128_CCM_8","TLS_ECDHE_ECDSA_WITH_CAMELLIA_128_GCM_SHA256","TLS_ECDHE_RSA_WITH_CAMELLIA_128_GCM_SHA256","TLS_DHE_RSA_WITH_CAMELLIA_128_GCM_SHA256","TLS_ECDHE_ECDSA_WITH_CAMELLIA_128_CBC_SHA256","TLS_ECDHE_RSA_WITH_CAMELLIA_128_CBC_SHA256","TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA256","TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA","TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA","TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA","TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA","TLS_DHE_PSK_WITH_AES_256_GCM_SHA384","TLS_DHE_PSK_WITH_AES_256_CCM","TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA384","TLS_DHE_PSK_WITH_AES_256_CBC_SHA384","TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA","TLS_DHE_PSK_WITH_AES_256_CBC_SHA","TLS_DHE_PSK_WITH_CAMELLIA_256_GCM_SHA384","TLS_ECDHE_PSK_WITH_CAMELLIA_256_CBC_SHA384","TLS_DHE_PSK_WITH_CAMELLIA_256_CBC_SHA384","TLS_PSK_DHE_WITH_AES_256_CCM_8","TLS_DHE_PSK_WITH_AES_128_GCM_SHA256","TLS_DHE_PSK_WITH_AES_128_CCM","TLS_ECDHE_PSK_WITH_AES_128_CBC_SHA256","TLS_DHE_PSK_WITH_AES_128_CBC_SHA256","TLS_ECDHE_PSK_WITH_AES_128_CBC_SHA","TLS_DHE_PSK_WITH_AES_128_CBC_SHA","TLS_DHE_PSK_WITH_CAMELLIA_128_GCM_SHA256","TLS_DHE_PSK_WITH_CAMELLIA_128_CBC_SHA256","TLS_ECDHE_PSK_WITH_CAMELLIA_128_CBC_SHA256","TLS_PSK_DHE_WITH_AES_128_CCM_8","TLS_ECDHE_PSK_WITH_3DES_EDE_CBC_SHA","TLS_DHE_PSK_WITH_3DES_EDE_CBC_SHA","TLS_RSA_WITH_AES_256_GCM_SHA384","TLS_RSA_WITH_AES_256_CCM","TLS_RSA_WITH_AES_256_CBC_SHA256","TLS_RSA_WITH_AES_256_CBC_SHA","TLS_ECDH_RSA_WITH_AES_256_GCM_SHA384","TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384","TLS_ECDH_RSA_WITH_AES_256_CBC_SHA","TLS_ECDH_ECDSA_WITH_AES_256_GCM_SHA384","TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384","TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA","TLS_RSA_WITH_AES_256_CCM_8","TLS_RSA_WITH_CAMELLIA_256_GCM_SHA384","TLS_RSA_WITH_CAMELLIA_256_CBC_SHA256","TLS_RSA_WITH_CAMELLIA_256_CBC_SHA","TLS_ECDH_RSA_WITH_CAMELLIA_256_GCM_SHA384","TLS_ECDH_RSA_WITH_CAMELLIA_256_CBC_SHA384","TLS_ECDH_ECDSA_WITH_CAMELLIA_256_GCM_SHA384","TLS_ECDH_ECDSA_WITH_CAMELLIA_256_CBC_SHA384","TLS_RSA_WITH_AES_128_GCM_SHA256","TLS_RSA_WITH_AES_128_CCM","TLS_RSA_WITH_AES_128_CBC_SHA256","TLS_RSA_WITH_AES_128_CBC_SHA","TLS_ECDH_RSA_WITH_AES_128_GCM_SHA256","TLS_ECDH_RSA_WITH_AES_128_CBC_SHA256","TLS_ECDH_RSA_WITH_AES_128_CBC_SHA","TLS_ECDH_ECDSA_WITH_AES_128_GCM_SHA256","TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA256","TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA","TLS_RSA_WITH_AES_128_CCM_8","TLS_RSA_WITH_CAMELLIA_128_GCM_SHA256","TLS_RSA_WITH_CAMELLIA_128_CBC_SHA256","TLS_RSA_WITH_CAMELLIA_128_CBC_SHA","TLS_ECDH_RSA_WITH_CAMELLIA_128_GCM_SHA256","TLS_ECDH_RSA_WITH_CAMELLIA_128_CBC_SHA256","TLS_ECDH_ECDSA_WITH_CAMELLIA_128_GCM_SHA256","TLS_ECDH_ECDSA_WITH_CAMELLIA_128_CBC_SHA256","TLS_RSA_WITH_3DES_EDE_CBC_SHA","TLS_ECDH_RSA_WITH_3DES_EDE_CBC_SHA","TLS_ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA","TLS_RSA_PSK_WITH_AES_256_GCM_SHA384","TLS_RSA_PSK_WITH_AES_256_CBC_SHA384","TLS_RSA_PSK_WITH_AES_256_CBC_SHA","TLS_RSA_PSK_WITH_CAMELLIA_256_GCM_SHA384","TLS_RSA_PSK_WITH_CAMELLIA_256_CBC_SHA384","TLS_RSA_PSK_WITH_AES_128_GCM_SHA256","TLS_RSA_PSK_WITH_AES_128_CBC_SHA256","TLS_RSA_PSK_WITH_AES_128_CBC_SHA","TLS_RSA_PSK_WITH_CAMELLIA_128_GCM_SHA256","TLS_RSA_PSK_WITH_CAMELLIA_128_CBC_SHA256","TLS_RSA_PSK_WITH_3DES_EDE_CBC_SHA","TLS_PSK_WITH_AES_256_GCM_SHA384","TLS_PSK_WITH_AES_256_CCM","TLS_PSK_WITH_AES_256_CBC_SHA384","TLS_PSK_WITH_AES_256_CBC_SHA","TLS_PSK_WITH_CAMELLIA_256_GCM_SHA384","TLS_PSK_WITH_CAMELLIA_256_CBC_SHA384","TLS_PSK_WITH_AES_256_CCM_8","TLS_PSK_WITH_AES_128_GCM_SHA256","TLS_PSK_WITH_AES_128_CCM","TLS_PSK_WITH_AES_128_CBC_SHA256","TLS_PSK_WITH_AES_128_CBC_SHA","TLS_PSK_WITH_CAMELLIA_128_GCM_SHA256","TLS_PSK_WITH_CAMELLIA_128_CBC_SHA256","TLS_PSK_WITH_AES_128_CCM_8","TLS_PSK_WITH_3DES_EDE_CBC_SHA","TLS_EMPTY_RENEGOTIATION_INFO_SCSV"]
  2017 - Evandro Copercini - Apache 2.0 License.
*/
#include <Arduino.h>
#include <WiFiClientSecure.h>

// const char* ssid     = "your-ssid";     // your network SSID (name of wifi network)
// const char* password = "your-password"; // your network password

const char* ssid = "esp8266";
const char* password = "forTheLoveOfEmbededSystem";

const char*  server = "https://industrialiot.onrender.com";  // Server URL

// www.howsmyssl.com root certificate authority, to verify the server
// change it to your server root CA
// SHA1 fingerprint is broken now!

// const char* test_root_ca= \
//      "-----BEGIN CERTIFICATE-----\n" \
//      "MIIDSjCCAjKgAwIBAgIQRK+wgNajJ7qJMDmGLvhAazANBgkqhkiG9w0BAQUFADA/\n" \
//      "MSQwIgYDVQQKExtEaWdpdGFsIFNpZ25hdHVyZSBUcnVzdCBDby4xFzAVBgNVBAMT\n" \
//      "DkRTVCBSb290IENBIFgzMB4XDTAwMDkzMDIxMTIxOVoXDTIxMDkzMDE0MDExNVow\n" \
//      "PzEkMCIGA1UEChMbRGlnaXRhbCBTaWduYXR1cmUgVHJ1c3QgQ28uMRcwFQYDVQQD\n" \
//      "Ew5EU1QgUm9vdCBDQSBYMzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEB\n" \
//      "AN+v6ZdQCINXtMxiZfaQguzH0yxrMMpb7NnDfcdAwRgUi+DoM3ZJKuM/IUmTrE4O\n" \
//      "rz5Iy2Xu/NMhD2XSKtkyj4zl93ewEnu1lcCJo6m67XMuegwGMoOifooUMM0RoOEq\n" \
//      "OLl5CjH9UL2AZd+3UWODyOKIYepLYYHsUmu5ouJLGiifSKOeDNoJjj4XLh7dIN9b\n" \
//      "xiqKqy69cK3FCxolkHRyxXtqqzTWMIn/5WgTe1QLyNau7Fqckh49ZLOMxt+/yUFw\n" \
//      "7BZy1SbsOFU5Q9D8/RhcQPGX69Wam40dutolucbY38EVAjqr2m7xPi71XAicPNaD\n" \
//      "aeQQmxkqtilX4+U9m5/wAl0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNV\n" \
//      "HQ8BAf8EBAMCAQYwHQYDVR0OBBYEFMSnsaR7LHH62+FLkHX/xBVghYkQMA0GCSqG\n" \
//      "SIb3DQEBBQUAA4IBAQCjGiybFwBcqR7uKGY3Or+Dxz9LwwmglSBd49lZRNI+DT69\n" \
//      "ikugdB/OEIKcdBodfpga3csTS7MgROSR6cz8faXbauX+5v3gTt23ADq1cEmv8uXr\n" \
//      "AvHRAosZy5Q6XkjEGB5YGV8eAlrwDPGxrancWYaLbumR9YbK+rlmM6pZW87ipxZz\n" \
//      "R8srzJmwN0jP41ZL9c8PDHIyh8bwRLtTcm1D9SZImlJnt1ir/md2cXjbDaJWFBM5\n" \
//      "JDGFoqgCWjBH4d1QB7wCCZAA62RjYJsWvIjJEubSfZGL+T0yjWW06XyxV3bqxbYo\n" \
//      "Ob8VZRzI9neWagqNdwvYkQsEjgfbKbYK7p2CNTUQ\n" \
//      "-----END CERTIFICATE-----\n";

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

// You can use x.509 client certificates if you want
//const char* test_client_key = "";   //to verify the client
//const char* test_client_cert = "";  //to verify the client


WiFiClientSecure client;

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(115200);
  delay(100);

  Serial.print("Attempting to connect to SSID: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  // attempt to connect to Wifi network:
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    // wait 1 second for re-trying
    delay(1000);
  }

  Serial.print("Connected to ");
  Serial.println(ssid);

  client.setCACert(test_root_ca);
  //client.setCertificate(test_client_cert); // for client verification
  //client.setPrivateKey(test_client_key);	// for client verification

  Serial.println("\nStarting connection to server...");
  if (!client.connect(server, 443))
    Serial.println("Connection failed!");
  else {
    Serial.println("Connected to server!");
    // Make a HTTP request:
    client.println("POST https://industrialiot.onrender.com/query HTTP/1.0");
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
    // if there are incoming bytes available
    // from the server, read them and print them:
    while (client.available()) {
      char c = client.read();
      Serial.write(c);
    }

    client.stop();
  }
}

void loop() {
  // do nothing
}
