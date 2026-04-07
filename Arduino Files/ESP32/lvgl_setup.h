#ifndef LVGL_SETUP_H
#define LVGL_SETUP_H

#include <lvgl.h>
#include <TFT_eSPI.h>

// Screen dimensions
extern const uint16_t screenWidth;
extern const uint16_t screenHeight;

// LVGL display buffer
extern lv_disp_draw_buf_t draw_buf;
extern lv_color_t buf[];

// TFT_eSPI instance
extern TFT_eSPI tft;

#if LV_USE_LOG != 0
void my_print(const char * buf);
#endif

void my_disp_flush( lv_disp_drv_t *disp, const lv_area_t *area, lv_color_t *color_p );
void my_touchpad_read( lv_indev_drv_t * indev_driver, lv_indev_data_t * data );
void lvgl_init_drivers();

#endif // LVGL_SETUP_H