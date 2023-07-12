#include <SPI.h>
#include <MFRC522.h>
#include <SoftwareSerial.h>

SoftwareSerial mySerial(10, 11);  // RX, TX

#define RST_PIN 9     // Reset pin
#define SS_PIN 10     // Slave select pin

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create an instance of the MFRC522 RFID reader

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  SPI.begin();        // Initialize SPI communication
  mfrc522.PCD_Init(); // Initialize the RFID reader

  //Serial.println("Ready to read RFID tags.");
}

void loop() {
  // Check if a new RFID tag is present
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    String rfidTag = "";

    // Read the tag data
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      rfidTag.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : ""));
      rfidTag.concat(String(mfrc522.uid.uidByte[i], HEX));
    }

    // Print the RFID tag on the serial monitor
    Serial.println(rfidTag);

    // Send the RFID tag to the Python script
    mySerial.println(rfidTag);

    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();
  }

  delay(1000);  // Add a delay if needed
}
