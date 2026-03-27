#include <lvgl.h>
#include <TFT_eSPI.h>
#include <ui.h>
#include "lvgl_setup.h" // Include the new setup file
#include "ui_update.h"
#include "ui_clock.h"

/*Don't forget to set Sketchbook location in File/Preferences to the path of your UI project (the parent foder of this INO file)*/

// Timeout for turning off the backlight if no serial data is received
const unsigned long SERIAL_TIMEOUT = 60000; // 60seconds
unsigned long last_serial_receive_time = 0;
bool backlight_on = true;

// Clock update timer
unsigned long last_time_update = 0;

void update_ui_elements();

void setup()
{
    Serial.begin( 115200 ); /* prepare for possible serial debug */
    randomSeed(analogRead(0));

    String LVGL_Arduino = "Hello Arduino! ";
    LVGL_Arduino += String('V') + lv_version_major() + "." + lv_version_minor() + "." + lv_version_patch();
    Serial.println( LVGL_Arduino );
    Serial.println( "I am LVGL_Arduino" );

    lvgl_init_drivers(); // Call the new initialization function

    ui_init();

    Serial.println( "Setup done" );
}

void loop()
{
    lv_timer_handler(); /* let the GUI do its work */
    delay( 5 );

    // Read incoming data from serial
    if (read_serial_data()) {
        last_serial_receive_time = millis();
        if (!backlight_on) {
            // Turn backlight on
            digitalWrite(TFT_BL, TFT_BACKLIGHT_ON);
            backlight_on = true;
        }
    }

    // Update all the UI elements with the new data
    update_ui_elements();

    // Check for serial timeout
    if (backlight_on && (millis() - last_serial_receive_time > SERIAL_TIMEOUT)) {
        // Turn backlight off
        digitalWrite(TFT_BL, !TFT_BACKLIGHT_ON);
        backlight_on = false;
    }
}