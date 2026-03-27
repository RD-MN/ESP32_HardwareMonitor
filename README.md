# ESP32 Hardware Monitor 🚀

A highly responsive, standalone ecosystem for monitoring PC hardware vitals (Temperatures, Wattage, Load, RPMs, and FPS) directly through an ESP32 TFT screen.

This project seamlessly bridges your PC hardware sensors with your external ESP32 screen using a lightweight, native, background Windows payload and robust Serial-over-USB communication.

## 🛠️ Features
- **Zero-GUI Windows Agent:** A silent, system-tray executable that reads real-time metrics natively via the Libre API.
- **Advanced Dynamic Hooks:** Analyzes and captures MSR data from CPU Temps, package Wattages, all the way to DirectX Fullscreen Framerates.
- **Intelligent Auto-Config:** Instantly scans and latches onto the target Arduino COMM Port natively without manual configuration.
- **Sleek Graphics:** TFT User Interface mapped gracefully out via SquareLine Studio powering an LVGL engine.
- **Silent Automations:** Integrated toggle menus to manipulate data poll rates and seamlessly hook into the Windows Task Scheduler for completely invisible boot automation.

## 📂 Project Setup
1. Open the Arduino IDE, compile, and flash your ESP32 using the `.ino` firmware in the hardware folder.
2. (Optional) Run the `BuildExec.bat` to seamlessly compile the Python source code into a standalone `.exe`.
3. Run `LHMToSerial.exe`. *(Note: It will request Administrator privileges once, to securely interface with the `PawnIO` kernel proxy driver needed for AMD/Intel thermal mapping).*
4. Check your hidden Taskbar tray—right-click the ESP32 Hardware Monitor icon to adjust **Refresh Rates** or enable **Run on Startup**!

---

## ⚖️ Open Source Acknowledgements & Licensing

This project is made possible through leveraging several incredible software layers. Massive thanks to the developers of the following ecosystems:

- **[LibreHardwareMonitor](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor)**
  - Handles the complex lower-level SMU/MSR subsystem sensor extraction natively.
  - Distributed freely under the **[Mozilla Public License 2.0 (MPL-2.0)](https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/blob/master/LICENSE)**. 

- **[SquareLine Studio](https://squareline.io/) & [LVGL](https://lvgl.io/)**
  - Used for the drag-and-drop creation of the C++ interface payload.
  - The C code itself operates on the core LVGL rendering graphics library, which is exclusively an Open-Source engine governed under the **[MIT License](https://github.com/lvgl/lvgl/blob/master/LICENCE.txt)**.

- **[Arduino Core Packages](https://www.arduino.cc/)**
  - C++ Compilation architecture leveraging LGPL underlying libraries.

### Primary Project License
The core functional bridging software of this project is proudly open-sourced under the **[MIT License](LICENSE)**. *(You can use it, edit it, and share it freely!)*
