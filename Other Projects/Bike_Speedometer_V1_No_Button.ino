#include <TM1637Display.h>
#include <math.h>

#define CLK 5
#define DIO 6
#define DGTL 4
#define ANLG A3

TM1637Display display (CLK, DIO);

float startOfProgram;
uint8_t numbers[10][1] = 
{ 
  {SEG_E | SEG_F}, //1
  {SEG_D | SEG_G | SEG_A | SEG_E | SEG_B}, //2
  {SEG_D | SEG_G | SEG_A | SEG_E | SEG_F}, //3
  {SEG_C | SEG_G | SEG_E | SEG_F}, //4
  {SEG_D | SEG_G | SEG_A | SEG_F | SEG_C}, //5
  {SEG_D | SEG_C | SEG_G | SEG_F | SEG_B | SEG_A}, //6
  {SEG_D | SEG_E | SEG_F}, //7
  {SEG_D | SEG_E | SEG_G | SEG_C | SEG_F | SEG_A | SEG_B}, //8
  {SEG_D | SEG_E | SEG_G | SEG_C | SEG_F}, //9
  {SEG_D | SEG_E | SEG_C | SEG_F | SEG_A | SEG_B}, //0
};

uint8_t numbersDecimal[][1] = //same thing except in binary and added 0x80 to turn on decimal
{
  {0xB0}, //10110000
  {0xDB}, //11011011
  {0xF9}, //11111001
  {0xF4}, //11110100
  {0xED}, //11101101
  {0xEF}, //11101111
  {0xB8}, //10111000
  {0xFF}, //11111111
  {0xFC}, //11111100
  {0xBF}, //10111111
};

void setup() {
  // put your setup code here, to run once:
  display.setBrightness(7);
  float startOfProgram = millis()/1000;
  Serial.begin(9600);
  display.clear();
  const uint8_t test[] = {0x80};
  display.setSegments(test, 1, 1);
}

class Display{
  private:
    float elapsedTime;
    float totalPauseTime;
  public:
    void displayStuff(float mphTemp){
      int mph = (int) mphTemp;
      int ones = mph%10;
      int tens = (mph - ones)/10;
      int tenths = int(mphTemp*10)-(int(mphTemp)*10);
      if (ones != 0){
        display.setSegments(numbers[ones-1], 1, 2);
      }
      else {
        display.setSegments(numbers[9], 1, 2);
      }
      if (tens != 0){
        display.setSegments(numbers[tens-1], 1, 3);
      }
      if (tenths != 0){
        display.setSegments(numbersDecimal[tenths-1], 1, 1);
      }
      else {
        display.setSegments(numbersDecimal[9], 1, 1);
      }
    }
    
    void findElapsedTime(){ //in seconds (if I did all the stupid calculations corectly which, lets be honest, I probably didn't)
      float currentTime;
      currentTime = millis()/1000;
      elapsedTime = (currentTime - totalPauseTime) - startOfProgram;
    }
};

class Speedometer
{
  private:
    const int wheelSize = 29;
    const float mpHalfRotate = ((((float)wheelSize/2.0)*3.14)/2.0)/63360.0; //miles per half rotation of wheel, or ~0.000359 mile
    float mph = 0;
    float lastPass = 0;
    float currentPass = 0;
    float deltaPass = 0;
    int analogPin;
    int digitalPin;
    bool prevOn = false; //previously on, yes or no
  public:
    Speedometer(int digitalPin, int analogPin){
      Speedometer::digitalPin = digitalPin;
      Speedometer::analogPin = analogPin;
      pinMode(digitalPin, INPUT);
      pinMode(analogPin, INPUT);
    }
    
    float getMPH(){
      return mph;
    }
    
    float timeTrack(){
      float currentTime = millis()/1000;
      return currentTime;
    }
    
    void readDSensor(){
      currentPass = timeTrack();
      if (digitalRead(digitalPin) == HIGH and not(prevOn)){ //only activates if it just was on
        lastPass = currentPass;
        prevOn = true;
        digitalWrite(LED_BUILTIN, LOW); //seeeduino XIAO led is inversed
      }
      else if (digitalRead(digitalPin) == LOW && prevOn) {
        prevOn = false;
        digitalWrite(LED_BUILTIN, HIGH);
      }
      deltaPass = currentPass - lastPass;
      processData();
    }
    
    void processData(){
      if (deltaPass >= 0.05){ //0.05s must pass before to guarantee no double readings, max speed is technically (INSERT NUMBER CUZ IM TOO TIRED AND LAZY ITS 21:43 RN) mph
        mph = (mpHalfRotate)/(deltaPass/3600.0);
      }
    }
};

Speedometer mySpdmtr (DGTL, ANLG);
Display myDisp;

void loop() {
  // put your main code here, to run repeatedly:
  mySpdmtr.readDSensor();
  myDisp.displayStuff(mySpdmtr.getMPH());
}
