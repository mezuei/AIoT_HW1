#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

// 網路與伺服器設定 (請補上您的 WiFi 登入資訊)
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// 請將此處 IP 替換為執行 Flask app.py 的電腦區域網路 IP
const String serverName = "http://192.168.X.X:5000/sensor";

// DHT 感測器設定
#define DHTPIN 4      // 定義 DHT11 連接的腳位 (可依據實際接線修改)
#define DHTTYPE DHT11 // 定義 DHT 型號
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if(WiFi.status() == WL_CONNECTED){
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    
    // 檢查是否讀取失敗
    if (isnan(humidity) || isnan(temperature)) {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }
    
    WiFiClient client;
    HTTPClient http;
    
    http.begin(client, serverName);
    http.addHeader("Content-Type", "application/json");
    
    // 組合 JSON 字串傳送給 Flask
    String httpRequestData = "{\"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + ", \"device_id\": \"ESP32_Real_Unit\", \"wifi_ssid\": \"" + String(ssid) + "\"}";
    
    int httpResponseCode = http.POST(httpRequestData);
    
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    
    http.end();
  }
  else {
    Serial.println("WiFi Disconnected");
  }
  delay(5000); // 每 5 秒傳送一次
}
