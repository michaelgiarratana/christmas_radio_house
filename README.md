# 🎄 Christmas Radio House

*A Raspberry Pi Pico-powered interactive holiday media player inspired by vintage Christmas broadcasts, seasonal storytelling, and the atmosphere of a classic Christmas living room.*

---

## Overview

The **Christmas Radio House** is a media device that inserts Christmas music, old-time radio programs, and holiday stories into any existing display piece, elevating your favorite holiday decoration.

Built around a Raspberry Pi Pico, DFPlayer Mini audio module, OLED display, and LED lights, the project is designed to recreate the feeling of gathering around a radio during the Christmas season. Rather than functioning as a conventional music player, the device serves as a piece of interactive holiday decor, providing curated seasonal ambience through audio, lighting, and physical controls.

---

## Features

-  Playback of Christmas music, radio broadcasts, and holiday stories
-  OLED "Now Playing" display
-  Simulated fireplace effect using PWM-controlled LEDs
-  Physical volume controls
-  Media category selection (Songs, Shows, Stories, etc.)
-  Track skipping
-  Randomized playback support
-  Sequential playback support
-  Fully offline operation with local media storage

---

## Demonstration

### Christmas Radio House in Operation

<!-- Replace with your own GIF -->

![Christmas Radio House Demo](examples/christmas_radio_house.gif)

---

## Repository Contents

### `candle_main.py`

The primary version of the project.

Features:

- Randomized playback within folders
- OLED display interface
- Folder navigation
- Volume adjustment
- Track skipping
- Dual-LED fireplace simulation

This version is intended to provide the most immersive and atmospheric experience.

---

### `random_main.py`

A simplified implementation focused on randomized playback behavior.

Useful when content variety and unpredictability are desired.

---

### `ordered_main.py`

A sequential playback implementation.

Tracks are played in a fixed order, making it suitable for curated playlists or narrative media collections.

---

### `dfplayer.py`

Control library for the DFPlayer Mini audio module (Credit: PenguinTutor).

Provides:

- Audio playback control
- Volume management
- Folder selection
- Track selection
- Serial communication interface

---

### `ssd1306.py`

MicroPython SSD1306 OLED display driver supporting I²C and SPI interfaces (Credit: stlehmann).

Used to display:

- Current media title
- Folder/category name
- Volume level
- System status information

---

## Hardware

The project was designed around the following components:

| Component | Description |
|-----------|-------------|
| Raspberry Pi Pico | Main controller |
| DFPlayer Mini | MP3 playback module |
| SSD1306 OLED Display | 128×64 display |
| MicroSD Card | Media storage |
| Push Buttons | User controls |
| Speaker | Audio output |
| LEDs | Simulated fireplace lighting |

---

## Media Organization

Content is organized into themed folders.

Example categories include:

| Folder | Contents |
|----------|----------|
| Songs | Traditional Christmas music |
| Shows | Vintage Christmas radio broadcasts |
| Stories | Classic holiday storytelling |

The software allows users to switch between categories while maintaining independent playback behavior within each collection.

---

## Project Philosophy

The goal of this project is not simply audio playback, but the recreation of a particular seasonal atmosphere.

Modern media devices emphasize convenience and unlimited choice. The Christmas Radio House instead embraces a slower and more intentional experience inspired by vintage radios, family living rooms, and the ambient media traditions of past Christmas seasons.

By combining physical controls, local media storage, subtle display elements, and simulated firelight, the project aims to function as both a technical build and a piece of interactive holiday decor.

---

## Future Development

Potential future enhancements include:

- [ ] Real-time clock support
- [ ] Scheduled playback modes
- [ ] Additional lighting effects
- [ ] Seasonal event scheduling
- [ ] Expanded media libraries
- [ ] Archive-style broadcast programming
- [ ] Weather and clock displays

---

## File Structure

```text
Christmas-Radio-House/
│
├── candle_main.py
├── random_main.py
├── ordered_main.py
├── dfplayer.py
├── ssd1306.py
│
└── README.md
```

---

## Contact

Questions, suggestions, or collaboration inquiries are welcome.

giarratanamd@gmail.com
