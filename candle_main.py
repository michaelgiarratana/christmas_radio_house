# Christmas Radio House - Auto-play + OLED Display + Volume & Folder Buttons
# MicroPython version with folder support, shuffle playback, and fireplace LED flicker

from machine import Pin, I2C, PWM
import ssd1306, time
from dfplayer import DFPlayerMini
import machine, random
from random import randint

print("Boot reason:", machine.reset_cause())

# ======== FIREPLACE LED SETUP ========
max_brightness = 65535
min_brightness = int(round(max_brightness / 2, 0))
max_sleep_time = 1000
min_sleep_time = 1000

# Two LEDs for a warmer "fire" effect
fire1 = PWM(Pin(15), freq=1000)
fire2 = PWM(Pin(14), freq=1000)

def flicker_fire():
    """Create random brightness for both LEDs to simulate flickering."""
    fire1.duty_u16(randint(min_brightness, max_brightness))
    fire2.duty_u16(randint(min_brightness, max_brightness))
    # no sleep here – flicker is driven by outer loop timing

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
btn_volup = Pin(10, Pin.IN, Pin.PULL_UP)
btn_voldown = Pin(11, Pin.IN, Pin.PULL_UP)
btn_folder = Pin(12, Pin.IN, Pin.PULL_UP)
btn_next = Pin(13, Pin.IN, Pin.PULL_UP)

def button_pressed(pin):
    if not pin.value():          
        time.sleep(0.05)
        return not pin.value()
    return False

# ======== INITIALIZE ========
volume = 18
df.set_volume(volume)
oled.fill(0)
oled.text("Christmas Radio", 0, 10)
oled.text("Initializing...", 0, 30)
oled.show()
time.sleep(1.5)

# ======== CUSTOM SHUFFLE FUNCTION ========
def shuffle_list(lst):
    shuffled = lst[:]
    for i in range(len(shuffled) - 1, 0, -1):
        j = random.randint(0, i)
        shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
    return shuffled

# ======== CONTENT ========
folders = {
    1: {"name": "Songs", "tracks": {
        1: {"title": "O Little Town", "duration": 97},
        2: {"title": "Silent Night", "duration": 187},
        3: {"title": "White Christmas", "duration": 93},
        4: {"title": "Oh Come All Ye", "duration": 132},
        5: {"title": "The First Noel", "duration": 149},
        6: {"title": "Joy To The World", "duration": 106},
        7: {"title": "The Christmas Song", "duration": 189},
        8: {"title": "Jingle Bells", "duration": 148},
        9: {"title": "It Came Upon", "duration": 87},
        10: {"title": "I'll Be Home", "duration": 180},
        11: {"title": "Silver Bells", "duration": 186},
    }},
    2: {"name": "Shows", "tracks": {
        1: {"title": "Walt Disney (1934)", "duration": 1790},
        2: {"title": "Looking For a Tree", "duration": 1756},
        3: {"title": "Early Xmas Gifts", "duration": 1763},
    }},
    3: {"name": "Stories", "tracks": {
        1: {"title": "A Wonderful Life", "duration": 3629},
        2: {"title": "Miracle on 34th", "duration": 3587},
    }}
}

current_folder = 1

# ======== DISPLAY ========
def show_now_playing(folder_name, track_title, track_num):
    oled.fill(0)
    oled.text("Now Playing", 0, 0)
    oled.text(folder_name, 0, 12)
    oled.text(track_title[:18], 0, 28)
    oled.text(f"T:{track_num} Vol:{volume}", 0, 50)
    oled.show()

# ======== MAIN LOOP ========
while True:
    folder = folders[current_folder]
    folder_name = folder["name"]
    tracks = folder["tracks"]
    track_nums = list(tracks.keys())

    # Shuffle once when entering a folder
    shuffled_tracks = shuffle_list(track_nums)
    current_index = 0
    print(f"Entered folder {current_folder}: {folder_name}, shuffled order {shuffled_tracks}")

    while True:
        track_num = shuffled_tracks[current_index]
        info = tracks[track_num]
        track_title = info["title"]
        duration = info["duration"]

        show_now_playing(folder_name, track_title, track_num)
        df.play(current_folder, track_num)
        print(f"Playing folder {current_folder} - track {track_num}: {track_title} ({duration}s)")

        restart_folder = False
        next_track = False

        for _ in range(duration * 10):  # 0.1s interval
            flicker_fire()  # 🔥 make the LEDs shimmer

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

            # --- Folder Change ---
            if button_pressed(btn_folder):
                current_folder += 1
                if current_folder > len(folders):
                    current_folder = 1
                print(f"Switched to folder {current_folder}: {folders[current_folder]['name']}")
                df.stop()
                restart_folder = True
                break

            # --- Next Button ---
            if button_pressed(btn_next):
                df.stop()
                next_track = True
                break

            time.sleep(0.1)

        df.stop()
        time.sleep(0.5)

        if restart_folder:
            break  # exit to outer loop (new folder will be initialized)

        if next_track or _ >= duration * 10 - 1:
            # Advance through shuffled order
            current_index += 1
            if current_index >= len(shuffled_tracks):
                # Reached end of playlist — reshuffle for new pass
                shuffled_tracks = shuffle_list(track_nums)
                current_index = 0
                print(f"Reshuffled folder {current_folder}: {shuffled_tracks}")
