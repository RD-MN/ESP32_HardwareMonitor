import tkinter as tk
from tkinter import ttk, messagebox
import settings_manager

# The available slots on the screen
SLOT_NAMES = [
    "Slot 1 (Left - Under CPU)", 
    "Slot 2 (Right - Under GPU)", 
    "Slot 3 (Left - Mid)", 
    "Slot 4 (Right - Mid)", 
    "Slot 5 (Left - Lower)", 
    "Slot 6 (Left - Bottom)"
]
SLOT_KEYS = ["slot1", "slot2", "slot3", "slot4", "slot5", "slot6"]

# Default formats mapping for standard slots
DEFAULT_FORMATS = {
    "slot1": "{} RPM",
    "slot2": "{} RPM",
    "slot3": "Ram: {} mb",
    "slot4": "Clock: {} MHz",
    "slot5": "VRam: {} mb",
    "slot6": "Case: {} RPM"
}

DEFAULT_SOURCES = {
    "slot1": "cpu_rpm",
    "slot2": "gpu_rpm",
    "slot3": "ram_used",
    "slot4": "gpu_clock",
    "slot5": "vram_used",
    "slot6": "case_rpm"
}

def load_all_sensors():
    try:
        # We temporarily initialize LHM to get the full list of sensors
        import LHMToSerial
        monitor = LHMToSerial.HardwareMonitor()
        _, all_sensors = monitor.get_sensors_data()
        monitor.close()
        # Sort keys
        return sorted(list(all_sensors.keys()))
    except Exception as e:
        print(f"Failed to load sensors: {e}")
        # Fallback list if LHM cannot be loaded without admin rights or something
        return sorted(list(set(DEFAULT_SOURCES.values())))

class ConfigApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hardware Monitor App")
        self.root.geometry("850x530")
        
        # Apply a slightly more modern default UI theme if available
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")
            
        self.apply_theme(style)
            
        import os, sys
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_path, "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(default=icon_path)
            except:
                pass
        
        # Load constraints
        self.sensors = ["STATIC_TEXT"] + load_all_sensors()
        self.config = settings_manager.load_config()
        self.mappings = self.config.get("mappings", {})
        
        self.vars_source = {}
        self.vars_format = {}
        
        # Instructions Header
        header_frame = ttk.Frame(root, style="Header.TFrame", padding=10)
        header_frame.pack(fill=tk.X)
        
        ttk.Label(header_frame, text="⚙️ Hardware Monitor App", font=("Segoe UI", 16, "bold")).pack(pady=(5, 0))
        ttk.Label(header_frame, text="Easily map your hardware sensors to the 6 text slots on your ESP32 display.", font=("Segoe UI", 10)).pack()
        ttk.Label(header_frame, text="Tip: Select a Data Type, or choose 'Custom' to manually format, using '{}' for the value (e.g. 'Speed: {} mbps').", font=("Segoe UI", 9, "italic")).pack(pady=(5, 0))
        
        # Main Mapping Frame
        frame = ttk.LabelFrame(root, text=" Screen Slot Mappings ", padding=15)
        frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Headers
        ttk.Label(frame, text="Display Slot", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=5, pady=(0, 10), sticky=tk.W)
        ttk.Label(frame, text="Hardware Sensor Source", font=("Segoe UI", 9, "bold")).grid(row=0, column=1, padx=5, pady=(0, 10), sticky=tk.W)
        ttk.Label(frame, text="Data Type / Format", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=5, pady=(0, 10), sticky=tk.W)
        
        # Separator line
        ttk.Separator(frame, orient='horizontal').grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 10))
        
        self.vars_type = {}
        self.vars_custom = {}
        COMMON_TYPES = ["RPM", "MB", "GB", "%", "°C", "W", "V", "MHz", "FPS", "Custom"]
        
        for i, (name, key) in enumerate(zip(SLOT_NAMES, SLOT_KEYS)):
            # Slot label
            ttk.Label(frame, text=name, font=("Segoe UI", 9)).grid(row=i+2, column=0, padx=5, pady=8, sticky=tk.W)
            
            # Data source combo
            src_var = tk.StringVar()
            saved_src = self.mappings.get(key, {}).get("source", DEFAULT_SOURCES.get(key, "STATIC_TEXT"))
            if saved_src not in self.sensors:
                self.sensors.append(saved_src)
            src_var.set(saved_src)
            
            cb = ttk.Combobox(frame, textvariable=src_var, values=self.sensors, width=65, state="readonly")
            cb.grid(row=i+2, column=1, padx=5, pady=8)
            self.vars_source[key] = src_var
            
            # Format entry
            saved_fmt = self.mappings.get(key, {}).get("format", DEFAULT_FORMATS[key])
            
            matched_type = "Custom"
            for t in COMMON_TYPES[:-1]: # Exclude "Custom"
                if saved_fmt == f"{{}} {t}" or saved_fmt.lower() == f"{{}} {t.lower()}":
                    matched_type = t
                    break
            
            type_var = tk.StringVar(value=matched_type)
            custom_var = tk.StringVar(value=saved_fmt)
            
            cell_frame = ttk.Frame(frame)
            cell_frame.grid(row=i+2, column=2, padx=5, pady=8, sticky=tk.W)
            
            cb_type = ttk.Combobox(cell_frame, textvariable=type_var, values=COMMON_TYPES, width=8, state="readonly")
            cb_type.pack(side=tk.LEFT, padx=(0, 5))
            
            ent_custom = ttk.Entry(cell_frame, textvariable=custom_var, width=15)
            
            if matched_type == "Custom":
                ent_custom.pack(side=tk.LEFT)
                
            def on_type_change(e, tv=type_var, cv=custom_var, ev=ent_custom):
                if tv.get() == "Custom":
                    ev.pack(side=tk.LEFT)
                else:
                    ev.pack_forget()
                    
            cb_type.bind("<<ComboboxSelected>>", on_type_change)
            
            self.vars_type[key] = type_var
            self.vars_custom[key] = custom_var
            
        # Buttons Frame
        btn_frame = ttk.Frame(root, padding=10)
        btn_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Define a consistent style for buttons
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Normal.TButton", font=("Segoe UI", 10))
        
        ttk.Button(btn_frame, text="Reset to Defaults", command=self.reset_defaults, style="Normal.TButton", width=18).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="🔍 Open LHM App", command=self.open_lhm, style="Normal.TButton", width=18).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="✅ Save & Apply", command=self.save_config, style="Accent.TButton", width=18).pack(side=tk.RIGHT, padx=10)
        
    def open_lhm(self):
        import os, subprocess, settings_manager
        lhm_exe = os.path.join(settings_manager.get_exe_dir(), "LHM", "LibreHardwareMonitor.exe")
        try:
            subprocess.Popen([lhm_exe])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open LHM:\n{e}\nPath: {lhm_exe}")
            
    def apply_theme(self, style):
        import winreg
        try:
            registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
            key = winreg.OpenKey(registry, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
            value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            is_dark = (value == 0)
        except Exception:
            is_dark = False

        if is_dark:
            bg_color = "#202020"
            fg_color = "#ffffff"
            entry_bg = "#333333"

            self.root.configure(bg=bg_color)
            
            # Switch to 'clam' as it handles dark mode recoloring better than Windows 'vista' natively
            style.theme_use('clam')
            
            style.configure('.', background=bg_color, foreground=fg_color, fieldbackground=entry_bg)
            style.configure('TFrame', background=bg_color)
            style.configure('Header.TFrame', background=bg_color)
            style.configure('TLabelframe', background=bg_color, foreground=fg_color)
            style.configure('TLabelframe.Label', background=bg_color, foreground=fg_color)
            style.configure('TLabel', background=bg_color, foreground=fg_color)
            style.configure('TSeparator', background="#444444")
            
            # Format Buttons specifically
            style.configure('TButton', background="#444444", foreground=fg_color, borderwidth=1)
            style.map('TButton', background=[('active', '#555555')])
            
            # Explicitly force TCombobox and TEntry to use the dark theme even in 'readonly' state
            style.configure('TEntry', fieldbackground=entry_bg, foreground=fg_color, insertcolor=fg_color)
            style.configure('TCombobox', fieldbackground=entry_bg, background=entry_bg, foreground=fg_color, arrowcolor=fg_color)
            
            style.map('TCombobox', 
                      fieldbackground=[('readonly', entry_bg), ('disabled', entry_bg)],
                      foreground=[('readonly', fg_color), ('disabled', '#888888')],
                      background=[('readonly', entry_bg)])
                      
            style.map('TEntry', 
                      fieldbackground=[('readonly', entry_bg), ('disabled', entry_bg)],
                      foreground=[('readonly', fg_color), ('disabled', '#888888')])
            
            # Combobox listbox drop down elements menu requires root option overrides
            self.root.option_add('*TCombobox*Listbox.background', entry_bg)
            self.root.option_add('*TCombobox*Listbox.foreground', fg_color)
            self.root.option_add('*TCombobox*Listbox.selectBackground', '#555555')
            self.root.option_add('*TCombobox*Listbox.selectForeground', fg_color)

    def reset_defaults(self):
        if messagebox.askyesno("Reset Defaults", "Are you sure you want to restore the original mappings?"):
            for key in SLOT_KEYS:
                self.vars_source[key].set(DEFAULT_SOURCES[key])
                saved_fmt = DEFAULT_FORMATS[key]
                
                matched_type = "Custom"
                for t in ["RPM", "MB", "GB", "%", "°C", "W", "V", "MHz", "FPS"]:
                    if saved_fmt == f"{{}} {t}" or saved_fmt.lower() == f"{{}} {t.lower()}":
                        matched_type = t
                        break
                        
                self.vars_type[key].set(matched_type)
                self.vars_custom[key].set(saved_fmt)
                
                # trigger event to show/hide custom text component
                self.vars_type[key].trace_vinfo() # this won't actually call the binding function without generate
                # Instead, we just hack a refresh for visibility: No manual pack_forget access here natively, 
                # but the user will likely hit save anyway, or we can just leave it as is if it's already "Custom".
                # To be totally robust we can force the event.
                self.root.event_generate("<<ComboboxSelected>>")

    def save_config(self):
        new_mappings = {}
        for key in SLOT_KEYS:
            tv = self.vars_type[key].get()
            if tv == "Custom":
                final_fmt = self.vars_custom[key].get()
            else:
                final_fmt = f"{{}} {tv}"
                
            new_mappings[key] = {
                "source": self.vars_source[key].get(),
                "format": final_fmt
            }
        
        self.config["mappings"] = new_mappings
        settings_manager.save_config(self.config)
        messagebox.showinfo("Success", "Configuration Saved Successfully!\nYour ESP32 display should update immediately.")
        self.root.destroy()

if __name__ == "__main__":
    import ctypes
    import sys
    # Make Windows DPI-aware for sharper text
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    # Force taskbar to not group this window under Python's default executable icon
    try:
        myappid = 'esphwm.configurator.ui.1' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except:
        pass
        
    root = tk.Tk()
    app = ConfigApp(root)
    root.mainloop()
