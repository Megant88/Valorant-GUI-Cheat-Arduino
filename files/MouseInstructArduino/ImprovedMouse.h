/*
  ImprovedMouse.h

  Copyright (c) 2023, khanxbahria
  Arduino Mouse library code originally Copyright (c) 2015, Arduino LLC
  Original code (pre-library) by Peter Barrett

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 2.1 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this library; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

  Modifications:
  - Added support for 16-bit axis in HID report
  - Removed scroll-wheel
  - Provided a method for transmitting raw HID reports
*/

#pragma once

#include <HID.h>

#include "AbstractMouse.h"

#if !defined(_USING_HID)

#warning "Using legacy HID core (non pluggable)"

#else


//================================================================================
//================================================================================
//  ImprovedMouse

class ImprovedMouse_ : public AbstractMouse
{
public:
  ImprovedMouse_();
  void begin();
  void end();
  uint8_t* makeReport(const int16_t& x, const int16_t& y) override;
  void sendRawReport(const uint8_t* reportData) override;
};
extern ImprovedMouse_ ImprovedMouse;

#endif
