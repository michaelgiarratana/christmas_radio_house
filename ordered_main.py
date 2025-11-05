# Christmas Radio House - Auto-play + OLED Display + Volume & Folder Buttons
# MicroPython version with folder support and safe button handling

from machine import Pin, I2C
import ssd1306, time
from dfplayer import DFPlayerMini
import machine

print("Boot reason:", machine.reset_cause())

# ======== CONFIGURATION ========
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
OLED_ADDR = 0x3c

# I2C setup for OLED
I2C_SCL_PIN = 3
I2C_SDA_PIN = 2
I2C_FREQ = 400000
i2c = I2C(1, scl=Pin(I2C_SCL_PIN), sda=Pin(I2C_SDA_PIN), freq=I2C_FREQ)
oled = ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c, addr=OLED_ADDR)

# DFPlayer setup
DF_TX = 4  # Pico TX → DFPlayer RX
DF_RX = 5  # Pico RX → DFPlayer TX
df = DFPlayerMini(1, DF_TX, DF_RX)
time.sleep(0.3)
df.stop()

# ======== BUTTON SETUP ========
btn_volup = Pin(10, Pin.IN, Pin.PULL_UP)    # GP10 → GND
btn_voldown = Pin(11, Pin.IN, Pin.PULL_UP)  # GP11 → GND
btn_folder = Pin(12, Pin.IN, Pin.PULL_UP)   # GP12 → GND
btn_next = Pin(13, Pin.IN, Pin.PULL_UP)     # GP13 → GND

def button_pressed(pin):
    if not pin.value():          # LOW when pressed
        time.sleep(0.05)         # 50ms debounce
        return not pin.value()
    return False

# ======== INITIALIZE ========
volume = 18  # 0–30
df.set_volume(volume)
oled.fill(0)
oled.text("Christmas Radio", 0, 10)
oled.text("Initializing...", 0, 30)
oled.show()
time.sleep(1.5)

# ======== CONTENT DICTIONARY ========
# Folder number → { "name": folder title, "tracks": {track_num: {title, duration}} }
folders = {
    1: {"name": "Shows", "tracks": {
        1: {"title": "Walt Disney (1934)", "duration": 1790},
    }},
    2: {"name": "Songs", "tracks": {
        1: {"title": "O Little Town", "duration": 97},
        2: {"title": "Silent Night", "duration": 187},
    }}
}

current_folder = 1
current_track = 1

# ======== DISPLAY FUNCTION ========
def show_now_playing(folder_name, track_title, track_num):
    oled.fill(0)
    oled.text("Now Playing", 0, 0)
    oled.text(folder_name, 0, 12)
    oled.text(track_title, 0, 28)
    oled.text(f"T:{track_num} Vol:{volume}", 0, 50)
    oled.show()

# ======== MAIN LOOP ========
while True:
    folder = folders[current_folder]
    folder_name = folder["name"]
    tracks = folder["tracks"]
    track_nums = list(tracks.keys())

    for track_num, info in tracks.items():
        track_title = info["title"]
        duration = info["duration"]

        show_now_playing(folder_name, track_title, track_num)
        df.play(current_folder, track_num)
        print(f"Playing folder {current_folder} - track {track_num}: {track_title} ({duration}s)")

        # Duration loop with safe button polling
        for _ in range(duration * 10):  # 0.1s loop
            # --- Volume Up ---
            if button_pressed(btn_volup):
                if volume < 30:
                    volume += 1
                    df.set_volume(volume)
                    show_now_playing(folder_name, track_title, track_num)
                    print(f"Volume increased to {volume}")
                time.sleep(0.1)

            # --- Volume Down ---
            if button_pressed(btn_voldown):
                if volume > 0:
                    volume -= 1
                    df.set_volume(volume)
                    show_now_playing(folder_name, track_title, track_num)
                    print(f"Volume decreased to {volume}")
                time.sleep(0.1)

            # --- Folder Cycle ---
            if button_pressed(btn_folder):
                current_folder += 1
                if current_folder > len(folders):
                    current_folder = 1
                # Break inner loop to restart playback from new folder
                print(f"Switched to folder {current_folder}: {folders[current_folder]['name']}")
                df.stop()
                break
            # --- Next Track ---
            if button_pressed(btn_next):
                track_index = track_nums.index(current_track)
                track_index = (track_index + 1) % len(track_nums)
                current_track = track_nums[track_index]
                print(f"Next track: {current_track}")
                df.stop()
                break

            time.sleep(0.1)  # regular sleep to check buttons ~10x/sec

        df.stop()
        time.sleep(0.5)
