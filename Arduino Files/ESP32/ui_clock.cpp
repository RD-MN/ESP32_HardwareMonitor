#include "ui_clock.h"
#include "ui.h"

unsigned int clock_minutes = 0;
unsigned int clock_hours = 0;

void update_clock_display() {
    if (ui_Clock) { // Check if the label has been created in SquareLine Studio
        lv_label_set_text_fmt(ui_Clock, "%02u:%02u", clock_hours, clock_minutes);
    }
}