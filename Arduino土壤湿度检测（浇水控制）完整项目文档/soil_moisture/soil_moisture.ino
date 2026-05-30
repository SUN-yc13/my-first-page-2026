int moisture;  // 土壤湿度
int dry = 590;
int middle = 398;   //中速
int wet = 396;
int relaypin = 2; //继电器引脚
int highWaterTime = 10*1000;  // 高档浇水时间（5秒，干土时）
int mediumWaterTime = 6000; // 中档浇水时间（2秒，中等湿度时）

void setup() {
  Serial.begin(9600);  //如果没有此代码，则无法通信
  pinMode(A1,INPUT);   //该代码可以使A0接受模式
  pinMode(relaypin, OUTPUT);   // D2为输出脚（控制继电器）
  digitalWrite(relaypin,LOW);  //继电器初始停止

}

void loop() {
  moisture =analogRead(A1); 
  Serial.print("土壤湿度量："); 
  Serial.println(moisture);
  (delay(1*1000));
  //优化三级干湿度判断，方便控制出水量
  if (moisture < 666) {
    if (moisture >= dry) {
      // 土壤干，执行高档浇水
      Serial.print("土壤较干，执行浇水：");
      digitalWrite(relaypin, HIGH);
      Serial.println("大功率浇水，时长10秒");
      delay(highWaterTime);
      digitalWrite(relaypin, LOW);
      Serial.println("over");
    }else if (moisture >= middle){
      // 土壤中等湿度，执行中档浇水（短时间浇水）
      digitalWrite(relaypin, HIGH);
      Serial.print("土壤较干，执行浇水：");
      Serial.println("中功率浇水，时长5秒");
      delay(mediumWaterTime); // 中档浇水2秒（可调整）
      digitalWrite(relaypin, LOW); // 浇水结束，关闭水泵
      Serial.println("over");
    } else if (moisture >= wet){
      // 土壤湿，停止浇水（防止烂根）
      digitalWrite(relaypin, LOW);
      Serial.println("over");
    }
  }
  delay(28800000);
}

