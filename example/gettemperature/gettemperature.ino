 /*!
  * @file  gettemperature.ino
  * @brief Gets the temperature of the module
  * @copyright   Copyright (c) 2020 DFRobot Co.Ltd (http://www.dfrobot.com)
  * @licence     The MIT License (MIT)
  * @author      KaixingPeng(kaixing.peng@dfrobot.com)
  * @version     V1.0
  * @date        2020-10-12
  * @get         from https://www.dfrobot.com
  */
#include "DFRobot_AmmoniaSensor.h"
//i2caddr
#define ADDRESS_0 0x74
#define ADDRESS_1 0x75
#define ADDRESS_2 0x76
#define ADDRESS_3 0x77

DFRobot_AmmoniaSensor myAmmoniaSensor(ADDRESS_3);

void setup(){
  Serial.begin(115200);
}

void loop() {
  Serial.print("temperature is: ");
  Serial.print(myAmmoniaSensor.getTemp());
  Serial.println("℃");
  delay(1000);
}
