#include <WiFi.h>
#include <Adafruit_ADS1015.h>

#include "esp_camera.h"
#include "soc/soc.h"           // Disable brownour problems
#include "soc/rtc_cntl_reg.h"  // Disable brownour problems
#include "driver/rtc_io.h"

#define HOME
#define DEBUG

#ifdef DEBUG
#define PRINTLN(x) Serial.println(x);
#define PRINT(x) Serial.print(x);
#define PRINTF(x, y) Serial.printf(x,y)
#else
#define PRINTLN(x)
#define PRINT(x)
#define PRINTF(x, y)
#endif


#define CAMERA_MODEL_AI_THINKER


// Pin definition for CAMERA_MODEL_AI_THINKER
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27

#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22


#define LED_PIN 33
#define FLASH_PIN 4
#define SDA_PIN 2
#define SCL_PIN 14

#define MAXC 100
#define BURST_SIZE 200

#ifdef HOME
/*const char *SSID = "MOVISTAR_8182";
  const char* WiFiPassword = "jwF4292858Pv25hQ332X";
*/
const char *SSID = "MOVISTAR_E380";
const char* WiFiPassword = "DFF9DD51C0B66A288CAC";
#else
const char *SSID = "dd-wrt";
const char* WiFiPassword = "ur_hack_la_salle";
#endif


const uint16_t port = 8018;
const char * host = "192.168.1.36";
//const char * host = "25.120.141.161";

const float ADC_MULTIPLIER = 0.1875F; /* ADS1115  @ +/- 6.144V gain (16-bit results) */
const float HUMIDITY_CONVERSION = 10.0F;

int connectWiFi();
void disconnectWiFi();
int connectToHost();
int takePicture(camera_fb_t **);
int sendImage(WiFiClient, camera_fb_t * );
int sendHumidity(WiFiClient, float);
int16_t readADC();
float adc2hum(float volts);
float hum2adc(float hum);


WiFiClient client;
Adafruit_ADS1115 ads;

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); //disable brownout detector

  Serial.begin(9600);

  pinMode(FLASH_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA; // FRAMESIZE_ + QVGA|CIF|VGA|SVGA|XGA|SXGA|UXGA
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  // Init Camera
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    PRINTF("Camera init failed with error 0x%x", err);
    return;
  }


  connectWiFi();
  while (connectToHost() < 0) {
    digitalWrite(LED_PIN, HIGH);
    delay(2000);
    digitalWrite(LED_PIN, LOW);
    PRINTLN("Waiting for Server");
  }

  //ADS Setup

  ads.setGain(GAIN_TWOTHIRDS);  // 2/3x gain +/- 6.144V  1 bit = 3mV      0.1875mV

  Wire.begin(SDA_PIN, SCL_PIN);

  PRINTLN("Setup done");
}



void loop() {
  int16_t adc_value = 0.0;
  float humidity = 0.0, volts = 0.0;
  int i = 0;
  camera_fb_t *fb = NULL;
  char data_read[MAXC];
  int option;



  /* for(i = 0; i < 10; i++){
     digitalWrite(LED_PIN, toggle);
     toggle = !toggle;
     adc_Value = readADC();
     PRINT("("); PRINT(adc_Value * ADC_MULTIPLIER); PRINTLN("mV)");
     delay(500);
    }
  */

  for (;;) {
    i = 0;
    while (client.available()) {
      data_read[i++] = client.read();
      PRINTF("Reading %d\n", data_read[0]);
    }
    if (i > 0) {
      option = (int)data_read[0];
      switch (option) {

        case 1: //IMAGE
          if (takePicture(&fb) < 0) {
            PRINTLN("[ERROR] Taking Picture");
          } else {
            if (sendImage(client, fb) < 0) {
              PRINTLN("[ERROR] Sending Image");
            }
            esp_camera_fb_return(fb);
          }
          break;

        case 2: //HUMIDITY
          adc_value = readADC();
          volts = adc_value * ADC_MULTIPLIER / 1000;
          humidity = adc2hum(volts);
          PRINT("("); PRINT(humidity); PRINTLN("%)");
          if (humidity <= 0) {
            humidity = 0;
            PRINTLN("[ERROR] ADC Value");
          } 
          if (sendHumidity(client, humidity) < 0) {
            PRINTLN("[ERROR] Sending Humidity");
          }
          break;

        case 3: //EXIT
          PRINTLN("Exit request.");
          disconnectWiFi();
          esp_deep_sleep_start();
          break;

        default:
          PRINTF("[ERROR] Wrong Option %d.", option);
          break;
      }
      client.flush();
    }
    PRINT("Waiting\n");
    delay(1000);
  }
  disconnectWiFi();
  for (;;);
}


void disconnectWiFi() {
  client.stop();
  WiFi.disconnect();
  PRINTLN("WiFi Disconnected.");
}


int connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, WiFiPassword);
  PRINT("Connecting to "); PRINTLN(SSID);

  uint8_t i = 0;
  while (WiFi.status() != WL_CONNECTED)
  {
    PRINT('.');
    delay(500);

    if ((++i % 16) == 0)
    {
      PRINTLN(F(" still trying to connect"));
    }
  }

  PRINT("Connected. My IP address is: ");
  PRINTLN(WiFi.localIP());
  return 0;
}

int connectToHost() {
  if (!client.connect(host, port)) {
    return -1;
  } else {
    PRINT("Connected to host\n")
  }
  return 0;
}

int takePicture(camera_fb_t ** fb) {
  digitalWrite(FLASH_PIN, HIGH);
  delay(50);
  *fb = esp_camera_fb_get();
  digitalWrite(FLASH_PIN, LOW);
  if (!(*fb)) return -1;
  return 0;
}

int sendImage(WiFiClient client, camera_fb_t * fb) {
  size_t length = 0;
  int packet_length = 500;
  int n_packets;
  int last_packet;
  int total_bytes = 0;
  int i = 0;
  int ok = 0;
  int nWritten = 0;


  PRINT("Length to send: ");
  PRINTLN(fb->len);

  do {
    client.print(fb->len);
    while (!client.available()) {
      PRINTLN("Waiting for OK response");
    }
    ok = client.read();
    PRINTLN("OK 1");
    while(total_bytes < fb->len){
      if(fb->len - total_bytes < packet_length){
        packet_length = fb->len - total_bytes;
      }
      nWritten = client.write(fb->buf + total_bytes, packet_length);
      total_bytes += nWritten;
      PRINTLN("")
    }
  } while (ok == 0);

  PRINTLN("Image sent");


  return 0;
}

int sendHumidity(WiFiClient client, float hum) {
  char ok = 0;
  char msg[MAXC];

  sprintf(msg, "%f", hum);
  PRINT("Message to send: ");
  PRINTLN(msg);


  do {
    client.print(msg);
    while (client.available() <= 0) {
      delay(100);  
    }
    ok = client.read();
  } while (ok != 1);

  return 0;
}

float adc2hum(float volts){
  float hum;
  
  if(volts < 0) volts*=-1;
  
  if(volts < 1.256){
    hum = -260.87*volts + 360.87;
  }else{
    hum = -8.9*volts + 44.3;
  }

  return hum;
}

float hum2adc(float hum){
  float volts;

  if(hum > 0 || hum > 100){
    return -1;
  }
  
  if(hum > 33.1){
    volts = (hum - 360.87)/(-260.87);
  }else{
    volts = (hum - 44.3)/(-8.9);
  }

  return volts;
}

int16_t readADC() {
  return ads.readADC_Differential_0_1();
}
