
//lux conversion script from known lux data 
void setup() {
  Serial.begin(9600);
}
int MAX_ADC_READING = 1023;
int ADC_REF_VOLTAGE = 3;
int resistorVoltage =0;
int ldrVoltage =0;
int ldrResistance =0;
int REF_RESISTANCE = 5;
int LUX_CALC_SCALAR =0;
int LUX_CALC_EXPONENT =0;
int ldrLux =0;

void loop() {
   int analogValue = analogRead(A0);
   resistorVoltage = (float)analogValue / MAX_ADC_READING * ADC_REF_VOLTAGE;
   ldrVoltage = ADC_REF_VOLTAGE - resistorVoltage;
   ldrResistance = ldrVoltage/resistorVoltage * REF_RESISTANCE;
   ldrLux = LUX_CALC_SCALAR * pow(ldrResistance, LUX_CALC_EXPONENT);
   Serial.println(ldrLux);
   delay(50);
 
  
  }  // the raw analog reading
