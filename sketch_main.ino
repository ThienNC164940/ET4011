#include <ESP8266WiFi.h>
#include <DHT.h>
#define DHTTYPE DHT11   

#define dht_dpin 2
DHT dht(dht_dpin, DHTTYPE); 

WiFiClient client;

String MakerIFTTT_Key ;
String MakerIFTTT_Event;
char *append_str(char *here, String s) {  int i=0; while (*here++ = s[i]){i++;};return here-1;}
char *append_ul(char *here, unsigned long u) { char buf[20]; return append_str(here, ultoa(u, buf, 10));}
char post_rqst[256];char *p;char *content_length_here;char *json_start;int compi;
void setup(void)
{ 
  dht.begin();
  Serial.begin(9600);
  WiFi.disconnect();
  delay(700);
  Serial.println("START");
   WiFi.begin("B10-508","khongbiet");
  while ((WiFi.status() == WL_CONNECTED)){
    delay(300);
    Serial.println("");

  }
  Serial.println("Connected");
  Serial.println("YOur IP is");
  Serial.println((WiFi.localIP().toString()));

}
void loop() {
    float g = analogRead(A0);
    Serial.print("Gas : ");
    Serial.println(g);
    float h = dht.readHumidity();
    float t = dht.readTemperature();         
    String MyString1 = "";
    String MyString2 = "";
    MyString1 = t; 
    MyString2 = h;
    if(isnan(h) || isnan(t) || isnan(g)){
      Serial.println("Failed dht");
      delay(30000);
      return;
    }
    Serial.print("Current humidity = ");
    Serial.print(h);
    Serial.print("%  ");
    Serial.print("temperature = ");
    Serial.print(t); 
    Serial.println("C  ");
    if (client.connect("maker.ifttt.com",80)) {
      MakerIFTTT_Key ="BtEDvbU92DxW8Pb0Zqlzb";
      MakerIFTTT_Event ="drive";
      p = post_rqst;
      p = append_str(p, "POST /trigger/");
      p = append_str(p, MakerIFTTT_Event);
      p = append_str(p, "/with/key/");
      p = append_str(p, MakerIFTTT_Key);
      p = append_str(p, " HTTP/1.1\r\n");
      p = append_str(p, "Host: maker.ifttt.com\r\n");
      p = append_str(p, "Content-Type: application/json\r\n");
      p = append_str(p, "Content-Length: ");
      content_length_here = p;
      p = append_str(p, "NN\r\n");
      p = append_str(p, "\r\n");
      json_start = p;
      p = append_str(p, "{\"value1\":\"");
      p = append_str(p, String(g));
      p = append_str(p, "\",\"value2\":\"");
      p = append_str(p, MyString1);
      p = append_str(p, "\",\"value3\":\"");
      p = append_str(p, MyString2);
      p = append_str(p, "\"}");

      compi= strlen(json_start);
      content_length_here[0] = '0' + (compi/10);
      content_length_here[1] = '0' + (compi%10);
      client.print(post_rqst);

    }
    delay(5000);
//    delay(800);
}
