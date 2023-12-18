#include "ImprovedMouse.h"
#include "HID-Project.h"

// pingCode should be greater than 0x07 to avoid conflicting with buttons mask
#define pingCode 0xf9

// RawHID Report Data size should equal to RAWHID_SIZE = 16
uint8_t rawhidData[RAWHID_SIZE];

bool clientConnected = false;

void flushRawHIDBuffer() {
  RawHID.enable();
}

bool checkPing() {
  if (rawhidData[0] == pingCode) {
    RawHID.write(rawhidData, sizeof(rawhidData));
    return true;
  } else return false;
}

void setup() {
  ImprovedMouse.begin();
  RawHID.begin(rawhidData, sizeof(rawhidData));
}

void loop() {
  if (!RawHID.available())
    return ;
  if (checkPing()) {
    clientConnected = true;
  } else if(clientConnected) {
    ImprovedMouse.sendRawReport(rawhidData);
  }
  flushRawHIDBuffer();
}