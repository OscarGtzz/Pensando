
#include <Arduino_LSM9DS1.h>

int fsrPin = 7;     // the FSR and 10K pulldown are connected to a0
int fsrReading;
float Gx, Gy, Gz, Ax, Ay, Az;

void setup() {
  Serial.begin(74880);
  while (!Serial);
  //Serial.println("Started");

  if (!IMU.begin()) {
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  //Serial.print("Accelerometer sample rate = ");
  //Serial.print(IMU.accelerationSampleRate());
  //Serial.println(" Hz");
  //Serial.println();
  //Serial.println("Acceleration in G's");
  //Serial.println("X\tY\tZ");
}

void loop() {
  float Ax, Ay, Az, Gx, Gy, Gz;
  fsrReading = analogRead(fsrPin);

  IMU.readGyroscope(Gx, Gy, Gz);
  IMU.readAcceleration(Ax, Ay, Az);
  
  Serial.print(map(Gx,-2000, 2000, -65536, 65536));
  Serial.print(',');
  Serial.print(map(Gy,-2000, 2000, -65536, 65536));
  Serial.print(',');
  Serial.print(map(Gz,-2000, 2000, -65536, 65536));
  Serial.print(',');
  Serial.print(mapfloat(Ax, -4, 4, -16384, 16384));
  Serial.print(',');
  Serial.print(mapfloat(Ay, -4, 4, -16384, 16384));
  Serial.print(',');
  Serial.print(mapfloat(Az, -4, 4, -16384, 16384));
  Serial.print(',');
  Serial.print(map(fsrReading, 0, 1023, 0, 4096));
  Serial.print("\n");
}


float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
 return (x * out_max)/4;
}
