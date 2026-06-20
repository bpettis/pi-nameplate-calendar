# SPDX-FileCopyrightText: 2019 Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
ePaper Display Shapes and Text demo using the Pillow Library.

"""
print("Started!")

import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.epd import Adafruit_EPD
#from adafruit_epd.uc8179 import Adafruit_UC8179

from adafruit_epd.uc8253 import Adafruit_UC8253_Tricolor


print("Finished Imports")

# First define some color constants
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)
RED = (0xFF, 0x00, 0x00)

# Next define some constants to allow easy resizing of shapes and colors
BORDER = 20
FONTSIZE = 24
BACKGROUND_COLOR = BLACK
FOREGROUND_COLOR = WHITE
TEXT_COLOR = RED

# create the spi device and pins we will need
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
srcs = None
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)



display = Adafruit_UC8253_Tricolor(240, 416,
    spi,
    cs_pin=ecs,
    dc_pin=dc,
    sramcs_pin=srcs,
    rst_pin=rst,
    busy_pin=busy
)

display.rotation = 1

width = display.width
height = display.height
image = Image.new("RGB", (width, height))


# clear the buffer
display.fill(Adafruit_EPD.WHITE)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# empty it
draw.rectangle((0, 0, width, height), fill=WHITE)


# First define some constants to allow easy resizing of shapes.
padding = 10
shape_width = 100
top = padding
bottom = height - padding


# Load default font.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
med_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
x_small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)

# Move left to right keeping track of the current x position for drawing shapes.
x = padding
# Draw a rectangle.
draw.rectangle((x, top, x + shape_width, bottom), outline=RED, fill=RED)

# Add some text
draw.text((x, top), "Hello", font=font, fill=BLACK)
draw.text((x, top + 40), "World!", font=font, fill=BLACK)





# Add an image for scheduling
overlay = Image.open("calendly_qr.png")


overlay = overlay.resize((75, 75), Image.BICUBIC)

# Paste into the lower right corner of the display
position = (display.width - overlay.width, display.height - overlay.height)
image.paste(overlay, position)

# Add the "Schedule a Meeting" text just to the left of the QR code
schedule_message = "Schedule a Meeting:"
draw.text((display.width - overlay.width - small_font.getsize(schedule_message)[0], display.height - (overlay.height // 2) - 2), schedule_message, font=small_font, fill=BLACK)


display.image(image)



display.display()

print("Done!")
