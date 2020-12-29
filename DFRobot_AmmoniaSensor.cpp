#include "DFRobot_AmmoniaSensor.h"

DFRobot_AmmoniaSensor::DFRobot_AmmoniaSensor(uint8_t i2caddr)
:_i2caddr(i2caddr)
{
  Wire.begin();
}

float DFRobot_AmmoniaSensor::getSlope(){
  uint8_t value = 0;
  i2cRead(GET_KEY_REGISTER,&value,1);
  if(value == 0){
    this->_Key = 14/100.0;
  }else{
    this->_Key =value / 1000.0;
  }
  return this->_Key;
}

float DFRobot_AmmoniaSensor::getAveragenum(float bArray[], uint8_t iFilterLen){
  uint8_t i = 0;
  double bTemp = 0;
  for(i = 0; i < iFilterLen; i++) {
    bTemp += bArray[i];
  }
  float Ammoniacon = bTemp / iFilterLen;
  float tem=getTemp();
  if((tem>=20)&&(tem<40))
    Ammoniacon=Ammoniacon/(0.036*tem+0.28);
  else if((tem>=-40)&&(tem<20))
    Ammoniacon=Ammoniacon/(1.1-0.005*tem);
  else
    ;
  if(flag){
    return (Ammoniacon - temperatureCompensation(tem));
  }
  return Ammoniacon;
}

float DFRobot_AmmoniaSensor::temperatureCompensation(float temp){
  float Compensation;
  if((temp>=20)&&(temp<40))
    Compensation=(2-10*temp);
  else if((temp>=-40)&&(temp<20))
    Compensation=(16.7-0.84*temp);
  else
    return 0.0;
  return Compensation;
}

float DFRobot_AmmoniaSensor::getAmmoniaconcentration(uint8_t CollectNum) 
{
  uint8_t rxbuf[10]={0}, k = 0;
  static uint8_t i = 0 ,j = 0;
  getSlope();
  if(CollectNum > 0) {
    for(j = CollectNum - 1;  j > 0; j--){
      AmmoniaData[j] = AmmoniaData[j-1];
    } 
    i2cRead(OXYGEN_DATA_REGISTER,rxbuf,3);
    AmmoniaData[0] = ((((float)rxbuf[0]) + ((float)rxbuf[1] / 10.0) + ((float)rxbuf[2] / 100.0))/(_Key));
    if(i < CollectNum)
      i++;
    float data=getAveragenum(AmmoniaData,i);
    if(data<0)
      return 0;
    else if((data>210)&&(data<300))
      return 888;
    else if(data>300)
      return 999;
  }else {
    return 0.0;
  }
}

float DFRobot_AmmoniaSensor::thermistor(int raw_ADC)
{
  uint32_t RBias =10000;
  float VBias=3.0;
  uint32_t ADC_BITS=1024;
  float THRM_DIV_VDC=0.0;
  float THRM_RES=0.0;
  float THRM_TEMP=0.0;
  
  THRM_DIV_VDC=0;
  THRM_RES=0;
  int THRM_ADC=raw_ADC;
  float THRM_A0 = -2.859169E+02;
  float THRM_A1 = 5.885114E-02;
  float THRM_A2 = -4.336183E-06;
  float THRM_A3 = 1.908142E-10;
  float THRM_A4 = -3.380032E-15;
  
  THRM_DIV_VDC=(VBias/ADC_BITS)*THRM_ADC;
  THRM_RES=THRM_DIV_VDC/((VBias-THRM_DIV_VDC)/RBias);
  THRM_TEMP=(THRM_A4*powf(THRM_RES,4))+(THRM_A3*powf(THRM_RES,3))+(THRM_A2*powf(THRM_RES,2))+(THRM_A1*THRM_RES)+THRM_A0;
  return THRM_TEMP;

}

float DFRobot_AmmoniaSensor::getTemp(){
  uint8_t buf[2];
  i2cRead(GET_LTEMP,buf,2);
  uint16_t temp=buf[0]+(buf[1]<<8);
  return thermistor(temp);
}

void DFRobot_AmmoniaSensor::tempCompensationswitch(eSwitch_t eSwitch){
  this->flag=eSwitch;
}

void DFRobot_AmmoniaSensor::i2cWrite(uint8_t regaddr,uint8_t*databuf,uint8_t len){
  Wire.beginTransmission(_i2caddr);
  Wire.write(regaddr);
  for(int i=0;i<len;i++){
    Wire.write(databuf[i]);
  }
  Wire.endTransmission();
}

uint8_t DFRobot_AmmoniaSensor::i2cRead(uint8_t regaddr,uint8_t*databuf,uint8_t len){
  Wire.beginTransmission(_i2caddr);
  Wire.write(regaddr);
  Wire.endTransmission();
  Wire.requestFrom(_i2caddr,len);
  if(Wire.available()){
    for(int i=0;i<len;i++){
      databuf[i]=Wire.read();
    }
  }
}