# DFRobot_AmmoniaSensor
DFRobot's DFRobot_AmmoniaSensor

## DFRobot_AmmoniaSensor Library for Arduino
---------------------------------------------------------
This is a library of ammonia sensors used to obtain the concentration of ammonia in the environment


## Table of Contents

* [Installation](#installation)
* [Methods](#methods)
* [Compatibility](#compatibility)
* [History](#history)
* [Credits](#credits)

<snippet>
<content>

## Installation

To use this library download the zip file, uncompress it to a folder named DFRobot_AmmoniaSensor.
Download the zip file first to use this library and uncompress it to a folder named DFRobot_AmmoniaSensor.

## Methods

```C++
 /*
  * @brief initialization parameters for i2c.
  * @param Wire is I2C Class
  * @param Alcohol_I2C_Address is i2c address
  */
  DFRobot_AmmoniaSensor myAmmoniaSensor(ADDRESS_3);

 /*
  * @Get module temperature
  */
  float getTemp();
  
 /*
  * @Get the ammonia concentration
  */
  float getAmmoniaconcentration(uint8_t CollectNum);
```
## Compatibility

MCU                | Work Well | Work Wrong | Untested  | Remarks
------------------ | :----------: | :----------: | :---------: | -----
FireBeetle-ESP32  |      √       |             |            | 
Arduino uno |       √      |             |            | 
FireBeetle-ESP8266  |      √       |              |             | 

## History

- October 12, 2020 - Version 1.0 released.


## Credits

Written by KaixingPeng(kaixing.peng@dfrobot.com), 2020. (Welcome to our [website](https://www.dfrobot.com/))