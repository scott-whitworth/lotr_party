//This is running on the Circuit Playground
// Needs corresponding python code to play the sounds on a computer

#include <Adafruit_CircuitPlayground.h> // https://github.com/adafruit/Adafruit_CircuitPlayground
#define cp CircuitPlayground //Got annoyed typing it out constantly
#include <Arduino.h>
#include <bluefruit.h>

//If you want debug messaged (not much there given the LEDs)
#define DEBUG false

//Define Cap touch threshold, used for all channels
#define CAP_THRESH 100

//Planning: 
// Seven capacitive touch (A1-6, TX)
// Button D4 / D5 - Not used, but we might want to. Not sure for what


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
#define endl "\n"

// Set up for NeoPixel's attached to this board
Adafruit_CPlay_NeoPixel neopixel = Adafruit_CPlay_NeoPixel(10,8); //10 lights, on pin 8

void setup() {
  //Turn on fast serial
  Serial.begin(115200);
  while(!Serial){
    delay(10);
  } //Wait for serial to pop up

  Serial << "Potatoes Test Code" << endl; //This occurs too fast, would need a display to show
  
  //Setting up Pixels
  neopixel.begin();
  neopixel.setBrightness(30);

  //Set Up CP object
  CircuitPlayground.begin();
  
  Serial << "Done with set up!" << endl;
}

//Pulled some info from: https://learn.adafruit.com/circuit-playground-fruit-drums/caternuson-tone-piano
uint8_t capPads[] = {3, 2, 0, 1, 6, 9, 10}; //Removed 12 (I think that is the audio signal)
uint8_t padLED[] =  {0, 1, 3, 4, 6, 8, 9 }; //Corresponding LEDs 
//      capValue ID: 0  1  2  3  4  5  6
int capValues[7];
bool capState[7];

void loop() {
  //Loop through Capacitive Touch Elements, get thier current reading
  for(int i = 0; i < 7; i++){
    capValues[i] = cp.readCap(capPads[i]); // Reference the capPads, pull value
  }

  //For each of the pulled in values, compare to the threshold, if pressed: do something!
  for(int i = 0; i < 7; i++){
    if( (capValues[i] > CAP_THRESH) && (!capState[i]) ){
      Serial << "Cap " << i << " has been pressed!" << endl;
      
      //Avoid the debugging filter, send "CAP:?" via serial
      Serial.print("CAP:");
      Serial.println(i);
      
      cp.setPixelColor(padLED[i],0,0,255); //Turn on corresponding LED

      capState[i] = true; //Helpful for toggling

    } else if ( (capValues[i] < CAP_THRESH) && (capState[i]) ) { //If we were previously pressed now we are not
      cp.setPixelColor(padLED[i],0,0,0);
      capState[i] = false;
    }
  }

  delay(100); //TODO: This might need some adjustment, seems good enough
}
