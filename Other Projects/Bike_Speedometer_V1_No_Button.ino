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
  {0x00}, //00000000
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
      else{
        display.setSegments(numbersDecimal[10], 1, 3);
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
      currentTime = millis()/1000.0;
      elapsedTime = (currentTime - totalPauseTime) - startOfProgram;
    }
};

class Speedometer
{
  private:
    //const float wheelSize = 29.0;
    //const float mpHalfRotate = ((wheelSize*3.14)/2.0)/63360.0; //miles per half rotation of wheel, or ~0.000359 mile
    const float mpHalfRotate = .00071859217;
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
      float currentTime = millis()/1000.0; //seconds
      return currentTime;
    }
    
    void readDSensor(){
      if (analogRead(analogPin) >= 825 and not(prevOn)){ //only activates if it just was on
        currentPass = timeTrack();
        lastPass = currentPass;
        prevOn = true;
        digitalWrite(LED_BUILTIN, LOW); //seeeduino XIAO led is inversed
      }
      else if (analogRead(analogPin) <= 825 && prevOn) {
        prevOn = false;
        digitalWrite(LED_BUILTIN, HIGH);
      }
      deltaPass = currentPass - lastPass;
      processData();
    }
    
    void processData(){
      mph = mpHalfRotate/(deltaPass/3600.0); //seconds to hours
    }
};

Speedometer mySpdmtr (DGTL, ANLG);
Display myDisp;
//float counter = 0.0;
void loop() {
  // put your main code here, to run repeatedly:
  mySpdmtr.readDSensor();
  myDisp.displayStuff(mySpdmtr.getMPH());
  //myDisp.displayStuff(counter += 0.1);

  //Serial.println(analogRead(A3));
}
