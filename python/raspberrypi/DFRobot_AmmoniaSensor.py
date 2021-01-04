# -*- coding: utf-8 -*
""" 
  @file DFRobot_AmmoniaSensor.py
  @note DFRobot_AmmoniaSensor Class infrastructure, implementation of underlying methods
  @copyright   Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @licence     The MIT License (MIT)
  @author      [ZhixinLiu](zhixin.liu@dfrobot.com)
  version  V1.0
  date  2020-5-27
  @get from https://www.dfrobot.com
  @url https://github.com/DFRobot/DFRobot_AmmoniaSensor
"""
import time
import smbus
import os
import math
           
ADDRESS_0                 = 0x74           # iic slave Address
ADDRESS_1                 = 0x75
ADDRESS_2                 = 0x76
ADDRESS_3                 = 0x77

OXYGEN_DATA_REGISTER      = 0x03           # Oxygen data register
USER_SET_REGISTER         = 0x08           # user set key value
AUTUAL_SET_REGISTER       = 0x09           # autual set key value
GET_KEY_REGISTER          = 0x0A           # get key value

GET_LTEMP                 = 0x0B
GET_HTEMP                 = 0x0C

class DFRobot_AmmoniaSensor(object):
  __key      = 0.0            # oxygen key value
  __count    = 0              # acquisition count
  __txbuf      = [0]          # iic send buffer
  __AmmoniaData = [0.00]*10      # ozone data
  flag = 1
  
  def __init__(self ,bus):
    self.i2cbus = smbus.SMBus(bus)

  def getSlope(self):
    global __key
    value = 0
    self.read_reg(GET_KEY_REGISTER,1)
    if(value == 0):
      self.__key = 14/100.0
    else:
      self.__key =value / 1000.0
    return self.__key

  def getTemp(self):
    buf=[0]*2
    buf=self.read_reg(GET_LTEMP,2)
    temp=buf[0]+(buf[1]<<8);
    return self.thermistor(temp);

  def thermistor(self,raw_ADC):
    RBias =10000;
    VBias=3.0;
    ADC_BITS=1024;
    THRM_DIV_VDC=0.0;
    THRM_RES=0.0;
    THRM_TEMP=0.0;
    THRM_DIV_VDC=0;
    THRM_RES=0;
    THRM_ADC=raw_ADC;
    THRM_A0 = -2.859169E+02;
    THRM_A1 = 5.885114E-02;
    THRM_A2 = -4.336183E-06;
    THRM_A3 = 1.908142E-10;
    THRM_A4 = -3.380032E-15;
    THRM_DIV_VDC=(VBias/ADC_BITS)*THRM_ADC;
    THRM_RES=THRM_DIV_VDC/((VBias-THRM_DIV_VDC)/RBias);
    THRM_TEMP=(THRM_A4*math.pow(THRM_RES,4))+(THRM_A3*math.pow(THRM_RES,3))+(THRM_A2*math.pow(THRM_RES,2))+(THRM_A1*THRM_RES)+THRM_A0;
    return THRM_TEMP;

  def tempCompensationswitch(self,eSwitch):
    self.flag=eSwitch

  def getAveragenum(self,bArray,iFilterLen):
    i = 0;
    bTemp = 0;
    for i in range(0,iFilterLen):
      bTemp += bArray[i]
    Ammoniacon = bTemp / iFilterLen
    tem=self.getTemp()
    if((tem>=20)and(tem<40)):
      Ammoniacon=Ammoniacon/(0.036*tem+0.28)
    elif((tem>=-40)and(tem<20)):
      Ammoniacon=Ammoniacon/(1.1-0.005*tem)
    if self.flag:
      return (Ammoniacon - self.temperatureCompensation(tem))
    return Ammoniacon
    
  def temperatureCompensation(self,temp):
    if((temp>=20)and(temp<40)):
      Compensation=(2-10*temp)
    elif((temp>=-40)and(temp<20)):
      Compensation=(16.7-0.84*temp)
    else:
      return 0.0
    return Compensation
    
  def getAmmoniaconcentration(self,collectnum):
    global __AmmoniaData
    self.getSlope()
    if collectnum > 0:
      for num in range(collectnum ,1 ,-1):
        self.__AmmoniaData[num-1] = self.__AmmoniaData[num-2]
      rslt=[0]*3  
      rslt = self.read_reg(OXYGEN_DATA_REGISTER ,3)
      self.__AmmoniaData[0] = (float(rslt[0]) + float(rslt[1]) / 10.0 + float(rslt[2]) / 100.0)/self.__key
      if self.__count < collectnum:
        self.__count += 1
      data=self.getAveragenum(self.__AmmoniaData ,self.__count)
      print("%f\n",data)
      if(data<0):
        return 0
      elif((data>210)and(data<300)):
        return 888
      elif(data>300):
        return 999
      else:
        return data
    elif (collectnum > 100) or (collectnum <= 0):
      return 0.0

'''
  @brief An example of an IIC interface module
'''
class DFRobot_AmmoniaSensor_IIC(DFRobot_AmmoniaSensor): 
  def __init__(self ,bus ,addr):
    self.__addr = addr;
    super(DFRobot_AmmoniaSensor_IIC, self).__init__(bus)

  '''
    @brief writes data to a register
    @param reg register address
    @param value written data
  '''
  def write_reg(self, reg, data):
    self.i2cbus.write_i2c_block_data(self.__addr ,reg ,data)

  '''
    @brief read the data from the register
    @param reg register address
    @param value read data
  '''
  def read_reg(self, reg ,len):
    while 1:
      try:
        rslt = self.i2cbus.read_i2c_block_data(self.__addr ,reg ,len)
        return rslt
      except:
        os.system('i2cdetect -y 1')