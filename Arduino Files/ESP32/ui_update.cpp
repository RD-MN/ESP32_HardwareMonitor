#include "ui_update.h"
#include "ui.h"
#include "ui_clock.h"
#include <Arduino.h>
#include <stdio.h> // Required for sscanf

// Global variables for sensor metrics
float cpu_temp = 0, gpu_temp = 0;
int cpu_percent = 0, gpu_percent = 0, cpu_watt = 0, gpu_watt = 0, fps = 0;

// Text buffers for configurable slots
char slot1_text[32] = "";
char slot2_text[32] = "";
char slot3_text[32] = "";
char slot4_text[32] = "";
char slot5_text[32] = "";
char slot6_text[32] = "";

/**
 * @brief Reads a delimited string of values from the serial port 
 *        and updates the global metric variables.
 */
bool read_serial_data() {
    if (Serial.available() > 0) {
        String line = Serial.readStringUntil('\n');

        // Parse: TIME|CPU%|CPUT|CPUW|GPU%|GPUT|GPUW|FPS|SLOT1|SLOT2|SLOT3|SLOT4|SLOT5|SLOT6
        int items_parsed = sscanf(line.c_str(), "%d:%d|%d|%f|%d|%d|%f|%d|%d|%31[^|]|%31[^|]|%31[^|]|%31[^|]|%31[^|]|%31[^\n]",
                                  &clock_hours, &clock_minutes, // Time
                                  &cpu_percent, &cpu_temp, &cpu_watt,
                                  &gpu_percent, &gpu_temp, &gpu_watt, &fps,
                                  slot1_text, slot2_text, slot3_text, slot4_text, slot5_text, slot6_text);

        if (items_parsed == 15) { // Expect 15 items
            return true; // Successfully parsed
        } else {
            return false; // Handle parsing errors
        }
    }
    return false;
}

/**
 * @brief Updates all the UI elements on the screen with the latest sensor data.
 */
void update_ui_elements() {
    lv_arc_set_value(ui_ArcCpu, cpu_percent);
    lv_arc_set_value(ui_ArcGpu, gpu_percent);
    lv_bar_set_value(ui_TempCpuBar, (int)cpu_temp, LV_ANIM_OFF);
    lv_bar_set_value(ui_TempGpuBar, (int)gpu_temp, LV_ANIM_OFF);

    lv_label_set_text_fmt(ui_cpuporc, "%d%%", cpu_percent);
    lv_label_set_text_fmt(ui_gpuporc, "%d%%", gpu_percent);
    lv_label_set_text_fmt(ui_fps, "%d FPS", fps);

    char temp_buf[10];
    dtostrf(cpu_temp, 4, 1, temp_buf);
    strcat(temp_buf, "°C");
    lv_label_set_text(ui_tempcpu, temp_buf);

    dtostrf(gpu_temp, 4, 1, temp_buf);
    strcat(temp_buf, "°C");
    lv_label_set_text(ui_tempgpu, temp_buf);
    
    // The fully customizable text slots natively injected from Python
    lv_label_set_text(ui_FanCpu, slot1_text);
    lv_label_set_text(ui_FanCpu1, slot2_text);
    lv_label_set_text(ui_RamUsage, slot3_text);
    lv_label_set_text(ui_GpuClock, slot4_text);
    lv_label_set_text(ui_VramUsage, slot5_text);
    lv_label_set_text(ui_FanCase, slot6_text);
    
    lv_label_set_text_fmt(ui_CPUW, "%d W", cpu_watt);
    lv_label_set_text_fmt(ui_GPUW1, "%d W", gpu_watt);

    // CPU Temp Color Change
    if (cpu_temp > 75) {
        lv_obj_set_style_text_color(ui_tempcpu, lv_color_hex(0xFF0000), LV_PART_MAIN);
        lv_obj_set_style_bg_color(ui_TempCpuBar, lv_color_hex(0xFF0000), LV_PART_INDICATOR);
    } else if (cpu_temp > 65) {
        lv_obj_set_style_text_color(ui_tempcpu, lv_color_hex(0xFFFF00), LV_PART_MAIN);
        lv_obj_set_style_bg_color(ui_TempCpuBar, lv_color_hex(0xFFFF00), LV_PART_INDICATOR);
    } else {
        lv_obj_set_style_text_color(ui_tempcpu, lv_color_hex(0xFFFFFF), LV_PART_MAIN);
        lv_obj_set_style_bg_color(ui_TempCpuBar, lv_color_hex(0x00FFFF), LV_PART_INDICATOR);
    }

    // GPU Temp Color Change
    if (gpu_temp > 70) {
        lv_obj_set_style_text_color(ui_tempgpu, lv_color_hex(0xFF0000), LV_PART_MAIN);
        lv_obj_set_style_bg_color(ui_TempGpuBar, lv_color_hex(0xFF0000), LV_PART_INDICATOR);
    } else if (gpu_temp > 60) {
        lv_obj_set_style_text_color(ui_tempgpu, lv_color_hex(0xFFFF00), LV_PART_MAIN);
        lv_obj_set_style_bg_color(ui_TempGpuBar, lv_color_hex(0xFFFF00), LV_PART_INDICATOR);
    } else {
        lv_obj_set_style_text_color(ui_tempgpu, lv_color_hex(0xFFFFFF), LV_PART_MAIN);
        lv_obj_set_style_bg_color(ui_TempGpuBar, lv_color_hex(0x00FFFF), LV_PART_INDICATOR);
    }

    update_clock_display();
}
