# -*- coding:utf-8 -*-
""" 
 /*!
  * @file  gettemperature.ino
  * @brief Gets ammonia concentration
  * @copyright   Copyright (c) 2020 DFRobot Co.Ltd (http://www.dfrobot.com)
  * @licence     The MIT License (MIT)
  * @author      KaixingPeng(kaixing.peng@dfrobot.com)
  * @version     V1.0
  * @date        2020-10-12
  * @get         from https://www.dfrobot.com
  */
"""
import sys
import time
import math
sys.path.append("../..")
from DFRobot_AmmoniaSensor import *

COLLECT_NUMBER   = 10              # collect number, the collection range is 1-100
IIC_MODE         = 0x01            # default use IIC1
'''
   # The first  parameter is to select iic0 or iic1
   # The second parameter is the iic device address
   # The default address for iic is ADDRESS_3
   # ADDRESS_0                 = 0x74
   # ADDRESS_1                 = 0x75
   # ADDRESS_2                 = 0x76
   # ADDRESS_3                 = 0x77
'''
AmmoniaSensor = DFRobot_AmmoniaSensor_IIC(IIC_MODE ,ADDRESS_3)
AmmoniaSensor_data=0.0
while(1):
  ''' Smooth data collection £¬the collection range is 1-100 '''
  AmmoniaSensor_data = AmmoniaSensor.getAmmoniaconcentration(COLLECT_NUMBER);
  print("AmmoniaSensor concentration is %4.2f ppm"%AmmoniaSensor_data)
  time.sleep(1)