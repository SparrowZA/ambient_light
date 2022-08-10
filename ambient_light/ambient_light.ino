/*
  Ambient Light controller code. This code is intended
  to be used with the ambient light Python application.

  Created 28 July 2022
  by Marc Geffroy

*/
#include <FastLED.h>
#define NUM_LEDS 60
#define DATA_PIN 3

#define BRIGHTNESS  64
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];

char PIXEL_ARR[256];
char SLIP_END     = 'D';
char SLIP_ESC     = 'E';
char SLIP_ESC_END = 'F';
char SLIP_ESC_ESC = 'G';

char *setup_msg = "Serial connected";

void setup() {
  // initialize serial:
  Serial.begin(115200);
  
  Serial.println(setup_msg);

  // Setup LEDs
  FastLED.addLeds<LED_TYPE, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS);
  //FastLED.setBrightness(  BRIGHTNESS );
}

void decodeSlip(char *baseStr, char const *pixelArr, int const bufferSize){
  int pixelCnt = 0;
  int baseCnt = 0;

  while(pixelCnt < bufferSize){
    if(pixelArr[pixelCnt] == SLIP_ESC && pixelArr[pixelCnt + 1] == SLIP_ESC_END){
      baseStr[baseCnt] = SLIP_END;
      pixelCnt++;
    }
    else if(pixelArr[pixelCnt] == SLIP_ESC && pixelArr[pixelCnt + 1] == SLIP_ESC_ESC){
      baseStr[baseCnt] = SLIP_ESC;
      pixelCnt++;
    }
    else{
      baseStr[baseCnt] = pixelArr[pixelCnt];
    }
    pixelCnt++;
    baseCnt++;
  }
}

void loop() {
  int led_chan;
  while(Serial.available()){
    size_t bufferSize = Serial.readBytesUntil('D', PIXEL_ARR, sizeof(PIXEL_ARR) - 1);
    // Decode slip arr
    char test [bufferSize];

    decodeSlip(test, PIXEL_ARR, bufferSize);

    // Write 
    for(int led=0; led < NUM_LEDS; led++){
      led_chan = led * 3;
      for(int colour_val=0; colour_val < 3; colour_val++){
         leds[led].r = PIXEL_ARR[led_chan];
         leds[led].g = PIXEL_ARR[led_chan + 1];
         leds[led].b = PIXEL_ARR[led_chan + 2];
      }
    }
    FastLED.show();
    Serial.flush();
    Serial.println(bufferSize);
    Serial.println(PIXEL_ARR);
    Serial.println(PIXEL_ARR);
    Serial.println();
    Serial.flush();
  }
}
