/******************************************************************************
* Zowi Battery Reader Library
* 
* @version 20150824
* @author Raul de Pablos Martin
*
******************************************************************************/
#ifndef __CLIENT_HANDLER_H__
#define __CLIENT_HANDLER_H__

#include "Arduino.h"
#include <ESP8266WiFi.h>

class ClientHandler
{
  const char* messageSeparator = "~";
  const char* headerSeparator = "&&";
public:
  WiFiClient client;
	ClientHandler(WiFiClient client){
	  this->client = client;
	};

	// readBatPercent
	double readBatVoltage(void);
	
	// readBatPercent
	double readBatPercent(void);
  
  void handleAction(String action, int pin, int value){
    if(action == "w" || action == "W"){
      pinMode(pin, OUTPUT);
      Serial.println("executing action");
      digitalWrite(pin, value);
      sendMessage("RESULT", "SUCCESS");
    }else{
      Serial.print("ERROR");
      digitalWrite(pin, value);
      sendMessage("RESULT", "ERROR");
    }
  };
  
  void sendMessage(String header, String message){
      client.print(header + headerSeparator + message + messageSeparator);
  };

  void listenLoop(){
    while(client.connected()){
      String message = client.readStringUntil('~');
      if(message != ""){
        Serial.println("");
        Serial.println(message);
        String action = message.substring(0,1);
        Serial.println(action);
        int pin = message.substring(2,4).toInt();
        Serial.println(pin);
        int value = message.substring(5).toInt();
        handleAction(action, pin, value);
      }
    }
  };

private:	

};

#endif // BATREADER_H //

