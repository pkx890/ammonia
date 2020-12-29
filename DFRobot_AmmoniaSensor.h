#include <Arduino.h>
#include <Wire.h>
#include <math.h>

#define  OCOUNT                100
#define  OXYGEN_DATA_REGISTER  0x03
#define  USER_SET_REGISTER     0x08
#define  AUTUAL_SET_REGISTER   0x09
#define  GET_KEY_REGISTER      0x0A

#define  GET_LTEMP             0x0B
#define  GET_HTEMP             0x0C

typedef enum {
  eSwitchOFF=0,
  eSwitchON
}eSwitch_t;

class DFRobot_AmmoniaSensor{
public:
  DFRobot_AmmoniaSensor(uint8_t i2caddr);
  ~DFRobot_AmmoniaSensor(){};
  float getSlope();
  float thermistor(int raw_ADC);
  float getTemp();
  float temperatureCompensation(float temp);
  float getAveragenum(float bArray[],uint8_t iFilterLen);
  void tempCompensationswitch(eSwitch_t eSwitch);
  float getAmmoniaconcentration(uint8_t CollectNum);
  void i2cWrite(uint8_t regaddr,uint8_t*databuf,uint8_t len);
  uint8_t i2cRead(uint8_t regaddr,uint8_t*databuf,uint8_t len);
private:
  uint8_t _i2caddr;
  float _Key;
  float AmmoniaData[OCOUNT] = {0.00};
  bool flag = 1;
};
