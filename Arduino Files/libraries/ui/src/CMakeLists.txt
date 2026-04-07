SET(SOURCES screens/ui_Screen1.c
    ui_theme_manager.c
    ui_themes.c
    ui.c
    components/ui_comp_hook.c
    ui_helpers.c
    images/ui_img_126065372.c
    fonts/ui_font_Clock.c
    fonts/ui_font_Font16_2.c
    fonts/ui_font_Test.c
    fonts/ui_font_Test16.c
    fonts/ui_font_Test18.c)

add_library(ui ${SOURCES})
