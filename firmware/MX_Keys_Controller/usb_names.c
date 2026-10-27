// USB manufacturer and product names shown by the host. These replace the Teensyduino
// defaults ("Teensyduino" / "Keyboard"), which the core declares as weak symbols.
// The vendor and product IDs are not changed here (they live in the Teensy core).
#include "usb_names.h"

#define MANUFACTURER_NAME     {'M','X',' ','K','e','y','s',' ','W','i','r','e','d'}
#define MANUFACTURER_NAME_LEN 13
#define PRODUCT_NAME          {'M','X',' ','K','e','y','s'}
#define PRODUCT_NAME_LEN      7

struct usb_string_descriptor_struct usb_string_manufacturer_name = {
  2 + MANUFACTURER_NAME_LEN * 2,
  3,
  MANUFACTURER_NAME
};

struct usb_string_descriptor_struct usb_string_product_name = {
  2 + PRODUCT_NAME_LEN * 2,
  3,
  PRODUCT_NAME
};
