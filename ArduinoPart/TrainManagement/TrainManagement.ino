/*
 * 
 * I2C Wire Part
 * SDA & SDC pins requiered
 *  
 * Hardware connected to UNO
 * 74HC595 shift register
 *
 * 
 * LCD Part
 * 
 * The circuit:
 * LCD RS pin to digital pin 13
 * LCD Enable pin to digital pin 12
 * LCD D4 pin to digital pin 11
 * LCD D5 pin to digital pin 10
 * LCD D6 pin to digital pin 9
 * LCD D7 pin to digital pin 8
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3) * 
 * 
 */

#include <LiquidCrystal.h>
#include <Wire.h>

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(13, 12, 11, 10, 9, 8);

String inputString = "";
boolean stringComplete = false;

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;

// UNO Pin to ShiftRegister
//Pin connected to ST_CP of 74HC595 (rclk)
int latchPin = 4;
//Pin connected to SH_CP of 74HC595
int clockPin = 3;
//Pin connected to DS of 74HC595
int dataPin = 6;
//Pin connected to OE of 74HC595
int oePin = 5;
//Pin connected to SRCLR of 74HC595
int srclrPin = 2;

void setup() {
  Serial.begin(9600);
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);

  // initialize the shift register pins
  pinMode(latchPin, OUTPUT);
  pinMode(dataPin, OUTPUT);  
  pinMode(clockPin, OUTPUT);
  pinMode(oePin, OUTPUT);  
  pinMode(srclrPin, OUTPUT);
  
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  Wire.onReceive(wireReceiveData);
  Wire.onRequest(wireSendData);

  // set to ready the ShiftRegister
  digitalWrite(oePin, LOW);
  digitalWrite(srclrPin, HIGH);

  printLine(0, "Welcome on");
  printLine(1, "Train Management");

  Serial.println("Train Management program initialized");
}

void loop() {
  delay(100);
}


////////////////////////////
// Shift Register part
void writeShiftRegister(byte data[]) {
  digitalWrite(latchPin, LOW);
  for (int i = 0, lenData = sizeof(data); lenData-- > 0; i++) {
    shiftOut(dataPin, clockPin, MSBFIRST, data[i]);
  }
  digitalWrite(latchPin, HIGH); 
}

////////////////////////////
// Wire function part
// callback for received data
void wireReceiveData(int byteCount){
  Serial.println("number of receiving bytes: " + String(byteCount));
  byte arrayData[byteCount + 1];
  arrayData[byteCount] = 0;
  int i = 0;
  while(Wire.available() && byteCount--) {
    int receiveChar = Wire.read();
    arrayData[i++] = receiveChar;
  }

  if(sizeof(arrayData) < 3) return;

  String strData = String((char*)arrayData);
  
  if(strData.substring(0,3) == "SR:" && sizeof(arrayData) >= 8) {
    // sending to Shift Register
    byte dataToSend[4];
    for(int j = 0; j < 4; j++) {
      dataToSend[j] = arrayData[j + 4];
    }
    writeShiftRegister(dataToSend);
  }
  else if (strData.substring(0,3) == "lcd") {
    // sending to lcd
    lcdPrint(strData);
  }

}

// callback for sending data
void wireSendData(){
    Wire.write(number);
}


///////////////////////////
// Serial (lcd) part
void clearLine(int lineNumber) {
  lcd.setCursor(0, lineNumber);
  lcd.print("                ");
}

void printLine(int lineNumber, String text) {
  lcd.setCursor(0, lineNumber);
  lcd.print(text);
}

void lcdPrint(String inputString) {
  int sizeOfCommand = inputString.length();
  if(sizeOfCommand > 7 && inputString.substring(0,3) == "lcd" && inputString.substring(5,7) == ":>") {
    int lcdLine = 0;
    // lcdl1:>line 1 on lcd
    // lcdl2:>line 2 on lcd
    int lineNb = ((char)inputString[4]) - 49;
    String txtContent = inputString.substring(7, (sizeOfCommand < 23) ? sizeOfCommand : 23);
    if(lineNb < 0 || lineNb > 1) lineNb = 0;
    clearLine(lineNb);
    printLine(lineNb, txtContent);
  }
  else {
    //Serial.println(inputString);
    String firstLine = inputString.substring(0,(sizeOfCommand < 16) ? sizeOfCommand : 16);
    clearLine(0);
    printLine(0, firstLine);
    if (sizeOfCommand > 15) {
      clearLine(1);
      printLine(1, inputString.substring(16,(sizeOfCommand < 32) ? sizeOfCommand : 32));
    }
  }
  Serial.println(inputString + " done\r\n");
}

/////////////////////////
// Serial Communication
void serialEvent(){
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }

  lcdPrint(inputString);

  // clear the string:
  inputString = "";
  stringComplete = false;
  Serial.flush();
}