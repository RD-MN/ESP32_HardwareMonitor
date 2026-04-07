import os
import sys
import json
import subprocess
from pystray import MenuItem, Menu

def get_exe_dir():
    """ Gets the true directory containing the executable, completely bypassing standard CWD. """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(sys.argv[0]))

CONFIG_FILE = os.path.join(get_exe_dir(), "config.json")

DEFAULT_CONFIG = {
    "poll_interval": 1.0,
    "run_on_startup": False
}

def get_exe_path():
    """ Get the precise path to the currently running executable or scripts. """
    if getattr(sys, 'frozen', False):
        return sys.executable
    else:
        return os.path.abspath(sys.argv[0])

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                conf = json.load(f)
                return {**DEFAULT_CONFIG, **conf}
        except:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")

# Global configuration store
config = load_config()

# --- STARTUP TASK MANAGEMENT ---
# The ONLY way to run as admin on startup silently without a UAC prompt
# is by creating a Windows Scheduled Task assigned to trigger At Log On.
TASK_NAME = "LHMToSerial_AutoStart"

def is_startup_enabled():
    return config.get("run_on_startup", False)

def toggle_startup(icon, item):
    new_state = not is_startup_enabled()
    exe_path = get_exe_path()
    
    # 0x08000000 = CREATE_NO_WINDOW
    creation_flags = 0x08000000
    
    if new_state:
        # Create scheduled task (Requires Admin permissions to run schtasks, which we have)
        # /RL HIGHEST triggers the maximum privileges explicitly, bypassing UAC
        cmd = f'schtasks /create /tn "{TASK_NAME}" /tr "\\"{exe_path}\\"" /sc onlogon /rl highest /f'
        try:
            subprocess.run(cmd, shell=True, check=True, creationflags=creation_flags)
            config["run_on_startup"] = True
            save_config(config)
        except Exception as e:
            print(f"Failed to create startup task: {e}")
    else:
        # Remove scheduled task
        cmd = f'schtasks /delete /tn "{TASK_NAME}" /f'
        try:
            subprocess.run(cmd, shell=True, check=True, creationflags=creation_flags)
            config["run_on_startup"] = False
            save_config(config)
        except Exception as e:
            print(f"Failed to delete startup task: {e}")

# --- REFRESH RATE MANAGEMENT ---
def set_refresh_rate(rate):
    def action(icon, item):
        config["poll_interval"] = rate
        save_config(config)
    return action

def get_refresh_rate():
    return config.get("poll_interval", 1.0)

def is_rate_checked(rate):
    def check(item):
        return get_refresh_rate() == rate
    return check

# --- CONFIGURATOR ---
def open_configurator(icon, item):
    exe_path = get_exe_path()
    try:
        if getattr(sys, 'frozen', False):
            subprocess.Popen([exe_path, "--config"])
        else:
            subprocess.Popen([sys.executable, exe_path, "--config"])
    except Exception as e:
        print(f"Error opening config: {e}")

# --- MENU GENERATOR ---
def get_menu_items(exit_action):
    # Available refresh rates (in seconds)
    rates = [0.5, 1.0, 2.0, 5.0]
    
    rate_items = []
    for r in rates:
        # radio=True groups them via visual pystray mechanics natively
        rate_items.append(
            MenuItem(f"{r} seconds", set_refresh_rate(r), checked=is_rate_checked(r), radio=True)
        )
        
    return Menu(
        MenuItem("Refresh Rate", Menu(*rate_items)),
        MenuItem("Open ESP32HWM Settings", open_configurator),
        MenuItem("Run at Startup", toggle_startup, checked=lambda item: is_startup_enabled()),
        MenuItem("Exit", exit_action)
    )
