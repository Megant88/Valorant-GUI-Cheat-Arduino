/*
    AbstractMouse.h
    Abstract HID Mouse class with 16 bit per movement axis
*/

#pragma once
#ifdef __AVR__
#include <stdint.h>
#else
#include <cstdint>
#endif

//================================================================================
//================================================================================
//    Mouse

#define MOUSE_DATA_SIZE 5

#define MOUSE_LEFT 1
#define MOUSE_RIGHT 2
#define MOUSE_MIDDLE 4
#define MOUSE_ALL (MOUSE_LEFT | MOUSE_RIGHT | MOUSE_MIDDLE)

class AbstractMouse
{
protected:
    uint8_t _buttons;
    void buttons(const uint8_t& b);
    virtual void sendRawReport(const uint8_t* reportData) = 0;
public:
    AbstractMouse();
    void click(const uint8_t& b = MOUSE_LEFT);
    void move(const int& x, const int& y);
    void press(const uint8_t& b = MOUSE_LEFT);     // press LEFT by default
    void release(const uint8_t& b = MOUSE_LEFT);   // release LEFT by default
    bool isPressed(const uint8_t& b = MOUSE_LEFT); // check LEFT by default
    virtual uint8_t* makeReport(const int16_t& x, const int16_t& y) = 0;
};
