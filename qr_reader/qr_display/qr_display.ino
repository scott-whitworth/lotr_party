//This is running on the Circuit Playground
// Needs corresponding python code to recieve character from QR scan

#include <Adafruit_CircuitPlayground.h> // https://github.com/adafruit/Adafruit_CircuitPlayground
#define cp CircuitPlayground //Got annoyed typing it out constantly
#include <Arduino.h>
#include <bluefruit.h>

//If you want debug messaged (not much there given the LEDs)
#define DEBUG true

// Support for printing normally
// https://forum.arduino.cc/t/text-and-variable-both-in-display-println/586907/4
template <typename T>
Print& operator<<(Print& printer, T value)
{
    if(DEBUG){
      printer.print(value);
    }
    return printer;
}
#define endl "\n\r"

// Set up for NeoPixel's attached to this board
Adafruit_CPlay_NeoPixel neopixel = Adafruit_CPlay_NeoPixel(10,8); //10 lights, on pin 8

void setup() {
  //Turn on fast serial
  Serial.begin(115200);
  while(!Serial){
    delay(10);
  } //Wait for serial to pop up

  Serial << "QR Test Code" << endl; //This occurs too fast, would need a display to show
  
  //Setting up Pixels
  neopixel.begin();
  neopixel.setBrightness(30);

  //Set Up CP object
  CircuitPlayground.begin();
  
  Serial << "Done with set up!" << endl;
}

void setAll(uint8_t r, uint8_t g, uint8_t b){
  for(int i = 0; i < 10; i++){
    neopixel.setPixelColor(i,r,g,b);
  }
  neopixel.show();
}

void loop() {

  String message = Serial.readStringUntil('\n');
  Serial << "Got new message: |" << message << "|" << endl;

  if(message.length() > 0){
    message.trim(); //This is to help unix line returns
    
    if(message == "Gimli"){
      setAll(255,0,0);
    } else if(message == "Gandalf"){
      setAll(0,255,0);
    } else if(message == "Frodo"){
      setAll(255,255,0);
    } else {
      setAll(0,0,255);
    }
  }

  delay(100); //TODO: This might need some adjustment, seems good enough
}
