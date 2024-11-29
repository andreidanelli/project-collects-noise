#include <WiFi.h>
#include <HTTPClient.h>
#include <NTPClient.h>
#include <WiFiUdp.h>

// Configurações de Wi-Fi
const char* ssid = "";
const char* password = "";

// Endereço do servidor Python
const char* serverUrl = "http://192.168.0.114:5000/upload";

const int sensor = 4;   // Pino D4 conectado ao sensor KY-037
const int LED = 19;  // Pino D19 conectado ao LED

// // Configuração do NTP
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org", -3 * 3600);  // Ajuste para UTC-3 (horário do Brasil)

void setup() {
  Serial.begin(115200);
  
  pinMode(sensor, INPUT);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);

  setup_wifi();
  timeClient.begin();  // Inicia cliente NTP
}

void loop() {
  // Se desconectar do WiFi, tenta reconectar
  if (WiFi.status() != WL_CONNECTED) {
    setup_wifi();
  }

  timeClient.update();  // Atualiza o horário via NTP

   if (digitalRead(sensor) == HIGH) {  // Ajuste o valor conforme a sensibilidade
    digitalWrite(LED, HIGH);
    delay(500);  // Luz de Alerta
    digitalWrite(LED, LOW);

    float volumeDB = calcularDecibeis(digitalRead(sensor));

    String csvData = gerarCSV(volumeDB);
    enviarDadosHTTP(csvData);

    delay(500);
  }
}

float calcularDecibeis(int leituraDigital) {
  return map(leituraDigital, 0, 4095, 30, 120);  // Ruído em dB
}

String gerarCSV(float volumeDB) {
  String dataHora = obterDataHora();
  long timestamp = millis();
  return "data_hora,volume_db,timestamp\n" + dataHora + "," + String(volumeDB) + "," + String(timestamp);
}

String obterDataHora() {
  time_t rawTime = timeClient.getEpochTime();
  struct tm* timeInfo = localtime(&rawTime);
  
  char buffer[20];
  strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", timeInfo);
  
  return String(buffer);
}

void setup_wifi() {
  Serial.println("Conectando ao WiFi...");
  
  while (WiFi.status() != WL_CONNECTED) {
    WiFi.begin(ssid, password);
    
    // Piscar LED enquanto conecta ao Wi-Fi
    digitalWrite(LED, HIGH);
    delay(500);
    digitalWrite(LED, LOW);
    delay(500);
    
    Serial.print(".");
  }
  
  Serial.println("\nWiFi conectado!");
  
  // Garantir que o LED fique desligado após a conexão
  digitalWrite(LED, LOW);
}

void enviarDadosHTTP(String csvData) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "text/csv");
    
    int httpResponseCode = http.POST(csvData);
    if (httpResponseCode > 0) {
      Serial.println("Dados enviados com sucesso!");
    } else {
      Serial.println("Erro ao enviar: " + String(httpResponseCode));
    }
    http.end();
  } else {
    Serial.println("WiFi desconectado!");
  }
}
