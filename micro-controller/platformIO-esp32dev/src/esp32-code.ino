#include <WiFi.h>
#include <WiFiClientSecure.h>

const char* ssid = "esp8266";
const char* password = "forTheLoveOfEmbededSystem";

const char* host = "industrialiot.onrender.com";
const int httpsPort = 443;

// Root certificate for the server
const char* rootCACertificate =  \
"-----BEGIN CERTIFICATE-----\n" \
"MIIFNDCCBNqgAwIBAgIQCC9vXhMOqjhjh/fFfICYmTAKBggqhkjOPQQDAjBKMQsw\n" \
"CQYDVQQGEwJVUzEZMBcGA1UEChMQQ2xvdWRmbGFyZSwgSW5jLjEgMB4GA1UEAxMX\n" \
"Q2xvdWRmbGFyZSBJbmMgRUNDIENBLTMwHhcNMjMwNDI1MDAwMDAwWhcNMjQwNDIz\n" \
"MjM1OTU5WjB1MQswCQYDVQQGEwJVUzETMBEGA1UECBMKQ2FsaWZvcm5pYTEWMBQG\n" \
"A1UEBxMNU2FuIEZyYW5jaXNjbzEZMBcGA1UEChMQQ2xvdWRmbGFyZSwgSW5jLjEe\n" \
"MBwGA1UEAxMVc25pLmNsb3VkZmxhcmVzc2wuY29tMFkwEwYHKoZIzj0CAQYIKoZI\n" \
"zj0DAQcDQgAESe3PljFfsfWY/UJwLvX39Es+PH0EnxrZ7LHXgwMpPmHuZnlWRW/j\n" \
"VVGdGnrc68bhtmIaSqyzTPvmGStQpoCgxKOCA3UwggNxMB8GA1UdIwQYMBaAFKXO\n" \
"N+rrsHUOlGeItEX62SQQh5YfMB0GA1UdDgQWBBQQqEe2OJuOgKxBzIYtfUWM0gbU\n" \
"iDA8BgNVHREENTAzghVzbmkuY2xvdWRmbGFyZXNzbC5jb22CGmluZHVzdHJpYWxp\n" \
"b3Qub25yZW5kZXIuY29tMA4GA1UdDwEB/wQEAwIHgDAdBgNVHSUEFjAUBggrBgEF\n" \
"BQcDAQYIKwYBBQUHAwIwewYDVR0fBHQwcjA3oDWgM4YxaHR0cDovL2NybDMuZGln\n" \
"aWNlcnQuY29tL0Nsb3VkZmxhcmVJbmNFQ0NDQS0zLmNybDA3oDWgM4YxaHR0cDov\n" \
"L2NybDQuZGlnaWNlcnQuY29tL0Nsb3VkZmxhcmVJbmNFQ0NDQS0zLmNybDA+BgNV\n" \
"HSAENzA1MDMGBmeBDAECAjApMCcGCCsGAQUFBwIBFhtodHRwOi8vd3d3LmRpZ2lj\n" \
"ZXJ0LmNvbS9DUFMwdgYIKwYBBQUHAQEEajBoMCQGCCsGAQUFBzABhhhodHRwOi8v\n" \
"b2NzcC5kaWdpY2VydC5jb20wQAYIKwYBBQUHMAKGNGh0dHA6Ly9jYWNlcnRzLmRp\n" \
"Z2ljZXJ0LmNvbS9DbG91ZGZsYXJlSW5jRUNDQ0EtMy5jcnQwDAYDVR0TAQH/BAIw\n" \
"ADCCAX0GCisGAQQB1nkCBAIEggFtBIIBaQFnAHUA7s3QZNXbGs7FXLedtM0TojKH\n" \
"Rny87N7DUUhZRnEftZsAAAGHula9PgAABAMARjBEAiAo1LKjZ7GCS4NtrQfPIBs7\n" \
"6Yl8IQoj2l3GrVjpZJeXyQIgVygiIxo/bKaP2cBPjNDDZ7SNRGNb8sxK/+jVixbq\n" \
"tEsAdgBz2Z6JG0yWeKAgfUed5rLGHNBRXnEZKoxrgBB6wXdytQAAAYe6Vr13AAAE\n" \
"AwBHMEUCIQCPtn6ZfB3otXJE96wo77OO0iDjDlBmptaFk3k3OzcC/AIgQvlAeNSV\n" \
"dmUu5h1mrBG3gLhftRL0xjy53P+Bwxo0tcQAdgBIsONr2qZHNA/lagL6nTDrHFIB\n" \
"y1bdLIHZu7+rOdiEcwAAAYe6Vr1eAAAEAwBHMEUCIFmI7nPYuSuGHakZvDf3sn5b\n" \
"ZVa25g1MesfH9GlwAOdIAiEA5WzCFrFe2pB8voAA/gpTwgXZ0WsnJMFBxIU/kjRP\n" \
"/wswCgYIKoZIzj0EAwIDSAAwRQIhANHGjpotdE3x+Roghod99sY8dKOHUuwrAI5U\n" \
"kyuiFa7MAiA/pxvobn/sikKd/YtnN6XQe+llfZskXNxVwXQWjodHAw==\n" \
"-----END CERTIFICATE-----\n";

void setup() {
  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // Create a WiFiClientSecure object
  WiFiClientSecure client;

  // Set the root certificate
  client.setCACert(rootCACertificate);

  // Connect to the server
  if (!client.connect(host, httpsPort)) {
    Serial.println("Connection failed!");
    return;
  }

  // Make an HTTP GET request
  client.print(String("GET /query HTTP/1.1\r\n") +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");

  Serial.println("Request sent!");

  // Wait for the response
  while (client.connected()) {
    String line = client.readStringUntil('\n');
    Serial.println(line);
  }

  Serial.println("Response received!");

  // Disconnect from the server
  client.stop();
}

void loop() {
  // Empty loop
}
