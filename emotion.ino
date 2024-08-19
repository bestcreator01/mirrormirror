// Title: Mirror, Mirror

#include <Adafruit_NeoPixel.h>
#define PIN 6
#define NUM_LEDS 40
#define BRIGHTNESS 8

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_LEDS, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  strip.begin();             // Initialize the strip
  strip.setBrightness(BRIGHTNESS);
  strip.show();              // Initialize all pixels to 'off'
  Serial.begin(9600);        // Start serial communication at 9600 baud rate
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the incoming command from the serial buffer
    setColor(command);
  }
}

void setColor(char command) {
  uint32_t color;

  switch (command) {
    case 'R': color = strip.Color(255, 0, 0); break;    // Red
    case 'G': color = strip.Color(0, 255, 0); break;    // Green
    case 'B': color = strip.Color(0, 0, 255); break;    // Blue
    case 'P': color = strip.Color(128, 0, 128); break;  // Purple
    case 'Y': color = strip.Color(255, 255, 0); break;  // Yellow (Neutral)
    default:  color = strip.Color(0, 0, 0);             // Default to off (or could set to neutral)
  }

  for(int i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, color);
  }
  strip.show();  // Update the strip with new settings
  delay(2000);  // Delay of 2 seconds
}
