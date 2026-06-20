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

# Move left to right keeping track of the current x position for drawing shapes.
x = padding
# Draw a rectangle.
draw.rectangle((x, top, x + shape_width, bottom), outline=RED, fill=RED)

# Add some text
draw.text((x, top), "Hello", font=font, fill=BLACK)
draw.text((x, top + 40), "World!", font=font, fill=BLACK)


# Add an image over everything
overlay = Image.open("blinka.png")

# Scale the image to the smaller screen dimension
image_ratio = overlay.width / overlay.height
screen_ratio = display.width / display.height
print(image_ratio, screen_ratio)
if screen_ratio < image_ratio:
    scaled_width = overlay.width * display.height // overlay.height
    scaled_height = display.height
else:
    scaled_width = display.width
    scaled_height = overlay.height * display.width // overlay.width


# Crop and center the image
x = scaled_width // 2 - display.width // 2
y = scaled_height // 2 - display.height // 2
overlay = overlay.crop((x, y, x + display.width, y + display.height)).convert("RGB")


position = (x, y)

# Paste the image over the image
# image.paste(overlay, position)

display.image(image)



display.display()

print("Done!")
