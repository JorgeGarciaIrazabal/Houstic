/*
 *  This sketch sends data via HTTP GET requests to data.sparkfun.com service.
 *
 *  You need to get streamId and privateKey at data.sparkfun.com and paste them
 *  below. Or just customize this script to talk to other HTTP servers.
 *
 */

#include <ESP8266WiFi.h>
#include "ClientHandler.h"

const char* ssid = "JAZZTEL_9A3B";
const char* password = "FA020156120757200985040689";
String name = "Caldera";

const char* host = "192.168.1.6";
int port = 7159;

void setup() {
  Serial.begin(115200);
  delay(10);
  pinMode(4,OUTPUT);

  // We start by connecting to a WiFi network

  Serial.println();
  Serial.println();
  Serial.print("Connecting to  ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  IPAddress ip(192, 168, 1, 29);
  IPAddress gateway(192, 168, 1, 1);
  IPAddress subnet(255, 255, 255, 0);
  WiFi.config(ip, gateway, subnet);
  int count = 0;
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    if(count++>30){
      setup();
      return;
    }
  }
  digitalWrite(4, HIGH);
  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  delay(1000);

  Serial.print("connecting to ");
  Serial.println(host);
  Serial.println(port);
  
  // Use WiFiClient class to create TCP connections
  ClientHandler clientHandler = ClientHandler(WiFiClient());
  if (!clientHandler.client.connect(host, port)) {
    Serial.println("connection failed");
    return;
  }
  
    Serial.println("ready to receive messages");
  clientHandler.sendMessage("ID", name);
  // Read all the lines of the reply from server and print them to Serial
  clientHandler.listenLoop();
  
  Serial.println();
  Serial.println("closing connection");
}



