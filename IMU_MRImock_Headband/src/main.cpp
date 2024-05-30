#include <Arduino.h>
#include <Wire.h>
#include "SparkFun_ISM330DHCX.h"

SparkFun_ISM330DHCX myISM; 

// Structs for X,Y,Z data
sfe_ism_data_t accelData; 
sfe_ism_data_t gyroData; 

unsigned long previousTime;

void setup(){
  Wire.begin();
  Serial.begin(115200);

  while (!myISM.begin())
  {
    Serial.println("ISM did not begin. Please check the wiring...");
    delay(1000);
  }

  // Reset the device to default settings. This is helpful if you're doing multiple
  // uploads testing different settings. 
  myISM.deviceReset();

  // Wait for it to finish resetting
  while( !myISM.getDeviceReset() ){ 
    delay(1);
  } 

  Serial.println("Reset.");
  Serial.println("Applying settings.");
  delay(100);
  
  myISM.setDeviceConfig();
  myISM.setBlockDataUpdate();
  
  // Set the output data rate and precision of the accelerometer
  myISM.setAccelDataRate(ISM_XL_ODR_104Hz);
  myISM.setAccelFullScale(ISM_4g); 

  // Set the output data rate and precision of the gyroscope
  myISM.setGyroDataRate(ISM_GY_ODR_104Hz);
  myISM.setGyroFullScale(ISM_250dps); 

  // Turn on the accelerometer's filter and apply settings. 
  myISM.setAccelFilterLP2();
  myISM.setAccelSlopeFilter(ISM_LP_ODR_DIV_100);

  // Turn on the gyroscope's filter and apply settings. 
  myISM.setGyroFilterLP1();
  myISM.setGyroLP1Bandwidth(ISM_MEDIUM);

  previousTime = millis();
}

void loop(){
  if(myISM.checkStatus()){
    myISM.getAccel(&accelData);
    myISM.getGyro(&gyroData);

    // Remove bias from acceleration data if needed (example values)
    float ax = accelData.xData - 0.0;
    float ay = accelData.yData - 0.0;
    float az = accelData.zData - 0.0; // Assuming stationary at the start, to remove gravity

    // Gyroscope data
    float gx = gyroData.xData;
    float gy = gyroData.yData;
    float gz = gyroData.zData;

    // Print in a format for the plotter
    Serial.print("AX:");
    Serial.print(ax);
    Serial.print(" AY:");
    Serial.print(ay);
    Serial.print(" AZ:");
    Serial.print(az);
    Serial.print(" GX:");
    Serial.print(gx);
    Serial.print(" GY:");
    Serial.print(gy);
    Serial.print(" GZ:");
    Serial.println(gz);
    delay(50);
  }
}

