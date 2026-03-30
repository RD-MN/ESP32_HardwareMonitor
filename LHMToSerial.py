import os
import sys

# Run as Administrator (UAC Prompt)
import ctypes
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit()

import time

import serial
import serial.tools.list_ports
import threading
from pystray import MenuItem as item
import pystray
from PIL import Image
import settings_manager

try:
    from pythonnet import load
    # Add LibreHardwareMonitorLib.dll via coreclr
    script_dir = os.path.dirname(os.path.abspath(__file__))
    lhm_dir = os.path.join(script_dir, "LHM")
    
    # Change working directory so LHM's dependent DLLs load correctly
    os.chdir(lhm_dir)
    sys.path.append(lhm_dir)
    
    runtime_config = os.path.join(lhm_dir, "LibreHardwareMonitor.runtimeconfig.json")
    if os.path.exists(runtime_config):
        load("coreclr", runtime_config=runtime_config)
        
    import clr # pythonnet MUST be imported AFTER pythonnet.load()
    clr.AddReference("LibreHardwareMonitorLib")
    from LibreHardwareMonitor.Hardware import Computer, HardwareType, SensorType
except Exception as e:
    print(f"FATAL: Could not load LibreHardwareMonitorLib.dll: {e}")
    sys.exit(1)

# --- CONFIGURATION ---
BAUDRATE = 115200

# --- GLOBAL STOP EVENT ---
stop_event = threading.Event()

class HardwareMonitor:
    def __init__(self):
        self.computer = Computer()
        self.computer.IsCpuEnabled = True
        self.computer.IsGpuEnabled = True
        self.computer.IsMemoryEnabled = True
        self.computer.IsMotherboardEnabled = True
        self.computer.IsControllerEnabled = True
        self.computer.IsNetworkEnabled = True
        self.computer.IsStorageEnabled = False
        
        try:
            self.computer.Open()
        except Exception as e:
            print(f"Failed to open hardware monitor: {e}")

    def close(self):
        try:
            self.computer.Close()
        except:
            pass

    def get_sensors_data(self):
        # Default starting values
        data = {
            'cpu_percent': 0, 'cpu_temp': 0.0, 'cpu_watt': 0,
            'gpu_percent_d3d': 0.0, 'gpu_percent_core': 0.0, 'gpu_temp': 0.0, 'gpu_watt': 0,
            'fps': 0,
            'cpu_rpm': 0, 'case_rpm': 0, 'gpu_rpm': 0, 'gpu_clock': 0, 'vram_used': 0, 'ram_used': 0
        }

        all_sensors = {}

        for hardware in self.computer.Hardware:
            hardware.Update()
            hw_type = hardware.HardwareType
            
            # Clean and abstract Network Adapters
            if hw_type == HardwareType.Network:
                name_low = hardware.Name.lower()
                if any(x in name_low for x in ["virtual", "vpn", "loopback", "pseudo", "vmware", "isatap", "bluetooth", "wsl", "veth", "hyper-v", "npcap", "pcap", "wan"]):
                    continue
                    
                is_wifi = "wi-fi" in name_low or "wireless" in name_low or "wlan" in name_low
                prefix = "wi-fi" if is_wifi else "ethernet"
                
                for sensor in hardware.Sensors:
                    if sensor.Value is not None:
                        sname = sensor.Name.lower().replace(" ", "_").replace("-", "_")
                        val = sensor.Value
                        
                        if "upload" in sname: sname = "upload_speed"
                        elif "download" in sname: sname = "download_speed"
                        elif "utilization" in sname: sname = "network_utilization"
                        else: continue
                        
                        key = f"{prefix}_{sname}"
                        all_sensors[key] = max(all_sensors.get(key, 0), sensor.Value)
                        
                continue # Skip generic processing for this hardware
            
            # Universal extraction for config
            for sub in getattr(hardware, 'SubHardware', []):
                sub.Update()
                for sensor in sub.Sensors:
                    if sensor.Value is not None:
                        key = f"{(hardware.Name + ' ' + sub.Name + ' ' + sensor.Name).lower().replace(' ', '_')}"
                        all_sensors[key] = sensor.Value
                        
            for sensor in hardware.Sensors:
                if sensor.Value is not None:
                    key = f"{(hardware.Name + ' ' + sensor.Name).lower().replace(' ', '_')}"
                    all_sensors[key] = sensor.Value

            # Motherboard (Fans usually under SuperIO subhardware)
            if hw_type == HardwareType.Motherboard:
                for sub in hardware.SubHardware:
                    for sensor in sub.Sensors:
                        if sensor.SensorType == SensorType.Fan and sensor.Value is not None:
                            val = int(sensor.Value)
                            name = sensor.Name.lower()
                            # Try to match Fan #2 and Fan #3 heuristics
                            if "fan #2" in name or "cpu" in name:
                                data['cpu_rpm'] = max(data['cpu_rpm'], val)
                            if "fan #3" in name or "sys" in name or "cha" in name:
                                data['case_rpm'] = max(data['case_rpm'], val)

            # CPU
            elif hw_type == HardwareType.Cpu:
                for sensor in hardware.Sensors:
                    if sensor.Value is None: continue
                    name = sensor.Name.lower()
                    if sensor.SensorType == SensorType.Load and "total" in name:
                        data['cpu_percent'] = int(sensor.Value)
                    elif sensor.SensorType == SensorType.Temperature:
                        if any(x in name for x in ["tctl/tdie", "core max", "package", "die", "core"]):
                            data['cpu_temp'] = max(data['cpu_temp'], float(sensor.Value))
                    elif sensor.SensorType == SensorType.Power:
                        if "package" in name or "power" in name or "cpu" in name:
                            data['cpu_watt'] = max(data['cpu_watt'], int(sensor.Value))

            # GPU
            elif hw_type in [HardwareType.GpuNvidia, HardwareType.GpuIntel, HardwareType.GpuAmd]:
                for sensor in hardware.Sensors:
                    if sensor.Value is None: continue
                    name = sensor.Name.lower()
                    if sensor.SensorType == SensorType.Load:
                        if "d3d 3d" in name:
                            data['gpu_percent_d3d'] = max(data['gpu_percent_d3d'], float(sensor.Value))
                        elif "core" in name:
                            data['gpu_percent_core'] = max(data['gpu_percent_core'], float(sensor.Value))
                    elif sensor.SensorType == SensorType.Temperature:
                        if any(x in name for x in ["hot spot", "core", "gpu"]):
                            data['gpu_temp'] = max(data['gpu_temp'], float(sensor.Value))
                    elif sensor.SensorType == SensorType.Fan:
                        data['gpu_rpm'] = max(data['gpu_rpm'], int(sensor.Value))
                    elif sensor.SensorType == SensorType.Power:
                        data['gpu_watt'] = max(data['gpu_watt'], int(sensor.Value))
                    elif sensor.SensorType == SensorType.Clock:
                        if "core" in name:
                            data['gpu_clock'] = max(data['gpu_clock'], int(sensor.Value))
                    elif sensor.SensorType == SensorType.Factor:
                        if "fps" in name:
                            data['fps'] = max(data['fps'], int(sensor.Value))
                    elif sensor.SensorType == SensorType.SmallData and "memory used" in name:
                        data['vram_used'] = int(sensor.Value)
                    elif sensor.SensorType == SensorType.Data and "memory used" in name:
                        if sensor.Value < 1000:
                            data['vram_used'] = int(sensor.Value * 1024)
                        else:
                            data['vram_used'] = int(sensor.Value)

            # Memory
            elif hw_type == HardwareType.Memory:
                for sensor in hardware.Sensors:
                    if sensor.Value is None: continue
                    name = sensor.Name.lower()
                    if sensor.SensorType == SensorType.Data and "memory used" in name:
                        data['ram_used'] = int(sensor.Value * 1024)

        # Merge backwards-compatible defaults into all_sensors so users can easily select standard mappings
        for k, v in data.items():
            if k not in all_sensors:
                all_sensors[k] = v
                
        all_sensors['cpu_percent'] = data['cpu_percent']
        all_sensors['cpu_temp'] = data['cpu_temp']
        all_sensors['cpu_watt'] = data['cpu_watt']
        all_sensors['gpu_percent'] = int(max(data['gpu_percent_d3d'], data['gpu_percent_core']))
        all_sensors['gpu_temp'] = data['gpu_temp']
        all_sensors['gpu_watt'] = data['gpu_watt']
        all_sensors['cpu_rpm'] = data['cpu_rpm']
        all_sensors['case_rpm'] = data['case_rpm']
        all_sensors['gpu_rpm'] = data['gpu_rpm']
        all_sensors['gpu_clock'] = data['gpu_clock']
        all_sensors['vram_used'] = data['vram_used']
        all_sensors['ram_used'] = data['ram_used']
        all_sensors['fps'] = data['fps']

        return data, all_sensors

def find_serial_port():
    """ Auto-detects a serial port """
    ports = serial.tools.list_ports.comports()
    
    # Priority 1: Specific hardware (Arduinos and specialized serial chips)
    for port, desc, hwid in ports:
        if any(keyword in desc.lower() for keyword in ["arduino", "ch340", "cp210", "ftdi"]):
            return port
             
    # Priority 2: Generic USB serial ports
    for port, desc, hwid in ports:
        if "usb" in desc.lower() and "serial" in desc.lower():
            return port

    # Fallback to the first available non-Bluetooth port
    if ports:
        non_bt_ports = [p.device for p in ports if "bluetooth" not in p.description.lower()]
        if non_bt_ports: return non_bt_ports[0]
        return ports[0].device
        
    return None

def run_serial_monitor(icon):
    serial_port = find_serial_port()
    if not serial_port:
        print("FATAL: No serial port found. Stopping.")
        icon.stop()
        return

    try:
        ser = serial.Serial(serial_port, BAUDRATE, timeout=1)
    except serial.SerialException as e:
        print(f"FATAL: Could not open serial port '{serial_port}'. Error: {e}")
        icon.stop()
        return

    icon.visible = True
    lhm_monitor = HardwareMonitor()

    while not stop_event.is_set():
        try:
            data, all_sensors = lhm_monitor.get_sensors_data()
            
            # Derived mappings for ARCs and Graphic indicators
            cpu_percent = data['cpu_percent']
            cpu_temp = int(data['cpu_temp'])
            cpu_watt = data['cpu_watt']
            
            gpu_percent = int(max(data['gpu_percent_d3d'], data['gpu_percent_core']))
            gpu_temp = int(data['gpu_temp'])
            gpu_watt = data['gpu_watt']
            fps = data['fps']
            
            current_time = time.strftime("%H:%M")
            
            # Configurable string slots
            mappings = settings_manager.load_config().get("mappings", {})
            import config_ui
            slots = []
            
            for key in config_ui.SLOT_KEYS:
                slot_cfg = mappings.get(key, {})
                default_src = config_ui.DEFAULT_SOURCES.get(key, "STATIC_TEXT")
                default_fmt = config_ui.DEFAULT_FORMATS.get(key, "")
                
                src = slot_cfg.get("source", default_src)
                fmt = slot_cfg.get("format", default_fmt)
                
                # Retrieve value
                val = ""
                if src != "STATIC_TEXT":
                    val = all_sensors.get(src, 0)
                    
                    if isinstance(val, float): val = int(val) # keep interface clean
                    
                if "{}" in fmt:
                    slot_str = fmt.replace("{}", str(val))
                else:
                    slot_str = fmt
                    
                # sanitize any pipes
                slots.append(slot_str.replace("|", ""))
                
            data_string = f"{current_time}|{cpu_percent}|{cpu_temp}|{cpu_watt}|{gpu_percent}|{gpu_temp}|{gpu_watt}|{fps}|{slots[0]}|{slots[1]}|{slots[2]}|{slots[3]}|{slots[4]}|{slots[5]}\n"
            
            ser.write(data_string.encode('utf-8'))
            
            # Dynamic sleep for POLLING based on user tray settings
            stop_event.wait(settings_manager.get_refresh_rate())
            
        except Exception as e:
            print(f"Loop error: {e}")
            ser.close()
            time.sleep(3)
            # Try reconnect logic
            new_port = find_serial_port()
            if new_port: serial_port = new_port
            try:
                ser = serial.Serial(serial_port, BAUDRATE, timeout=1)
            except:
                stop_event.wait(10)
            
    if ser.is_open:
        ser.close()
    lhm_monitor.close()

def exit_action(icon, item):
    stop_event.set()
    icon.stop()

def setup(icon):
    threading.Thread(target=run_serial_monitor, args=(icon,), daemon=True).start()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = script_dir
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    if "--config" in sys.argv:
        import config_ui
        import tkinter as tk
        root = tk.Tk()
        app = config_ui.ConfigApp(root)
        root.mainloop()
        sys.exit(0)
        
    try:
        image = Image.open(resource_path("icon.ico"))
        menu = settings_manager.get_menu_items(exit_action)
        icon = pystray.Icon("ESP32 Hardware Monitor", image, "ESP32 Hardware Monitor", menu)
        icon.run(setup)
    except FileNotFoundError:
        print("Error: icon.ico not found. Please create an icon file.")
        
        # Fallback if no icon to still run
        # Make a dummy invisible run if needed?
        print("Running in console fallback due to missing icon...")
        # create a dummy image to not completely crash, or just don't use pystray
        dummy_image = Image.new('RGB', (64, 64), (255, 255, 255))
        menu = settings_manager.get_menu_items(exit_action)
        icon = pystray.Icon("ESP32 Hardware Monitor", dummy_image, "ESP32 Hardware Monitor", menu)
        icon.run(setup)
    except Exception as e:
        print(f"An error occurred: {e}")
