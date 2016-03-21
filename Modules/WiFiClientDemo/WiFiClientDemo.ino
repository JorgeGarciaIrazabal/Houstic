/*
 *  This sketch sends data via HTTP GET requests to data.sparkfun.com service.
 *
 *  You need to get streamId and privateKey at data.sparkfun.com and paste them
 *  below. Or just customize this script to talk to other HTTP servers.
 *
 */

#include <ESP8266WiFi.h>

const char* ssid = "JAZZTEL_9A3B";
const char* password = "FA020156120757200985040689";

const char* host = "192.168.1.6";
int port = 7159;

void handleAction(String action, int pin, int value){
  if(action == "w" || action == "W"){
    pinMode(pin, OUTPUT);
    Serial.println("executing action");
    digitalWrite(pin, value);
  }else{
    Serial.print("ERROR");
    digitalWrite(pin, value);
  }
}


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
  // the dns server ip
  IPAddress ip(192, 168, 1, 29);
  // the router's gateway address:
  IPAddress gateway(192, 168, 1, 1);
  // the subnet:
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

int value = 0;

void loop() {
  delay(1000);
  ++value;

  Serial.print("connecting to ");
  Serial.println(host);
  Serial.println(port);
  
  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    return;
  }
  
    Serial.println("ready to receive messages");
  client.println("I am esp8266");
  // Read all the lines of the reply from server and print them to Serial
  while(client.connected()){
    String message = client.readStringUntil('~');
    if(message != ""){
      Serial.println("");
      Serial.println(message);
      String action = message.substring(0,1);
      Serial.println(action);
      int pin = message.substring(2,4).toInt();
      Serial.println(pin);
      value = message.substring(5).toInt();
      Serial.println(value);
      handleAction(action, pin, value);
    }
  }
  
  Serial.println();
  Serial.println("closing connection");
}



