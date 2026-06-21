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
from datetime import datetime

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
shape_width = display.width - padding * 2
top = padding + 10
bottom = height - padding


# Load default font.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
med_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
x_small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)

# Move left to right keeping track of the current x position for drawing shapes.
x = padding


def do_not_disturb():

    ## DO NOT DISTURB SIGN ##

    # Draw a rectangle.
    draw.rectangle((x, top, x + shape_width, top + 50), outline=RED, fill=RED)

    # Put text in the rectangle, centered vertically and horizontally in the rectangle.
    status_message = "Do Not Disturb"
    draw.text((x + (shape_width // 2) - (font.getbbox(status_message)[2] // 2), top + (50 // 2) - (font.getbbox(status_message)[3] // 2)), status_message, font=font, fill=WHITE)

    # Add a small line of text below the rectangle, centered horizontally with the rectangle.
    sub_message = "I will yap and yap if given the opportunity..."
    draw.text((x + (shape_width // 2) - (small_font.getbbox(sub_message)[2] // 2), top + 50 + padding), sub_message, font=small_font, fill=BLACK)

    # Add a small horizontal line underneath all that
    draw.line((x, top + 60 + small_font.getbbox(sub_message)[3], x + shape_width, top + 60 + small_font.getbbox(sub_message)[3]), fill=BLACK, width=2)


def in_a_meeting():
    ## IN A MEETING SIGN ##

    # Draw a rectangle.
    draw.rectangle((x, top, x + shape_width, top + 50), outline=BLACK, fill=BLACK)

    # Put text in the rectangle, centered vertically and horizontally in the rectangle.
    status_message = "In a Meeting"
    draw.text((x + (shape_width // 2) - (font.getbbox(status_message)[2] // 2), top + (50 // 2) - (font.getbbox(status_message)[3] // 2)), status_message, font=font, fill=RED)

    # Add a small line of text below the rectangle, centered horizontally with the rectangle.
    sub_message = "Please do not disturb me unless it's an emergency."
    draw.text((x + (shape_width // 2) - (small_font.getbbox(sub_message)[2] // 2), top + 50 + padding), sub_message, font=small_font, fill=BLACK)

    # Add a small horizontal line underneath all that
    draw.line((x, top + 60 + small_font.getbbox(sub_message)[3], x + shape_width, top + 60 + small_font.getbbox(sub_message)[3]), fill=BLACK, width=2)

def available():
    ## AVAILABLE SIGN ##

    # Draw a rectangle.
    draw.rectangle((x, top, x + shape_width, top + 50), outline=BLACK, fill=BLACK)

    # Put text in the rectangle, centered vertically and horizontally in the rectangle.
    status_message = "Available"
    draw.text((x + (shape_width // 2) - (font.getbbox(status_message)[2] // 2), top + (50 // 2) - (font.getbbox(status_message)[3] // 2)), status_message, font=font, fill=WHITE)

    # Add a small line of text below the rectangle, centered horizontally with the rectangle.
    sub_message = "Feel free to stop by and chat!"
    draw.text((x + (shape_width // 2) - (small_font.getbbox(sub_message)[2] // 2), top + 50 + padding), sub_message, font=small_font, fill=BLACK)

    # Add a small horizontal line underneath all that
    draw.line((x, top + 60 + small_font.getbbox(sub_message)[3], x + shape_width, top + 60 + small_font.getbbox(sub_message)[3]), fill=BLACK, width=2)

def working_remotely():
    ## WORKING REMOTELY SIGN ##

    # Draw a rectangle.
    draw.rectangle((x, top, x + shape_width, top + 50), outline=BLACK, fill=BLACK)

    # Put text in the rectangle, centered vertically and horizontally in the rectangle.
    status_message = "Working Remotely"
    draw.text((x + (shape_width // 2) - (font.getbbox(status_message)[2] // 2), top + (50 // 2) - (font.getbbox(status_message)[3] // 2)), status_message, font=font, fill=WHITE)

    # Add a small line of text below the rectangle, centered horizontally with the rectangle.
    sub_message = "Please email me if you need anything."
    draw.text((x + (shape_width // 2) - (small_font.getbbox(sub_message)[2] // 2), top + 50 + padding), sub_message, font=small_font, fill=BLACK)

    # Add a small horizontal line underneath all that
    draw.line((x, top + 60 + small_font.getbbox(sub_message)[3], x + shape_width, top + 60 + small_font.getbbox(sub_message)[3]), fill=BLACK, width=2)


def out_of_office():
    ## OUT OF OFFICE SIGN ##

    # Draw a rectangle.
    draw.rectangle((x, top, x + shape_width, top + 50), outline=BLACK, fill=BLACK)

    # Put text in the rectangle, centered vertically and horizontally in the rectangle.
    status_message = "Out of Office"
    draw.text((x + (shape_width // 2) - (font.getbbox(status_message)[2] // 2), top + (50 // 2) - (font.getbbox(status_message)[3] // 2)), status_message, font=font, fill=WHITE)

    # Add a small line of text below the rectangle, centered horizontally with the rectangle.
    sub_message = "I may have limited access to email, but I will respond as soon as I can."
    draw.text((x + (shape_width // 2) - (small_font.getbbox(sub_message)[2] // 2), top + 50 + padding), sub_message, font=small_font, fill=BLACK)

    # Add a small horizontal line underneath all that
    draw.line((x, top + 60 + small_font.getbbox(sub_message)[3], x + shape_width, top + 60 + small_font.getbbox(sub_message)[3]), fill=BLACK, width=2)

def here_but_busy():
    ## HERE BUT BUSY SIGN ##

    # Draw a rectangle.
    draw.rectangle((x, top, x + shape_width, top + 50), outline=BLACK, fill=BLACK)

    # Put text in the rectangle, centered vertically and horizontally in the rectangle.
    status_message = "Here, But Busy"
    draw.text((x + (shape_width // 2) - (font.getbbox(status_message)[2] // 2), top + (50 // 2) - (font.getbbox(status_message)[3] // 2)), status_message, font=font, fill=RED)

    # Add a small line of text below the rectangle, centered horizontally with the rectangle.
    sub_message = "Please knock only if it's urgent."
    draw.text((x + (shape_width // 2) - (small_font.getbbox(sub_message)[2] // 2), top + 50 + padding), sub_message, font=small_font, fill=BLACK)

    # Add a small horizontal line underneath all that
    draw.line((x, top + 60 + small_font.getbbox(sub_message)[3], x + shape_width, top + 60 + small_font.getbbox(sub_message)[3]), fill=BLACK, width=2)

def office_hours():
    ## OFFICE HOURS SIGN ##

    # Draw a rectangle.
    draw.rectangle((x, top, x + shape_width, top + 50), outline=BLACK, fill=BLACK)

    # Put text in the rectangle, centered vertically and horizontally in the rectangle.
    status_message = "Office Hours"
    draw.text((x + (shape_width // 2) - (font.getbbox(status_message)[2] // 2), top + (50 // 2) - (font.getbbox(status_message)[3] // 2)), status_message, font=font, fill=WHITE)

    # Add a small line of text below the rectangle, centered horizontally with the rectangle.
    sub_message = "Come on in! I'm here to help."
    draw.text((x + (shape_width // 2) - (small_font.getbbox(sub_message)[2] // 2), top + 50 + padding), sub_message, font=small_font, fill=BLACK)

    # Add a small horizontal line underneath all that
    draw.line((x, top + 60 + small_font.getbbox(sub_message)[3], x + shape_width, top + 60 + small_font.getbbox(sub_message)[3]), fill=BLACK, width=2)


def somewhere_else():
    ## SOMEWHERE ELSE SIGN ##

    # Draw a rectangle.
    draw.rectangle((x, top, x + shape_width, top + 50), outline=BLACK, fill=BLACK)

    # Put text in the rectangle, centered vertically and horizontally in the rectangle.
    status_message = "Somewhere Else"
    draw.text((x + (shape_width // 2) - (font.getbbox(status_message)[2] // 2), top + (50 // 2) - (font.getbbox(status_message)[3] // 2)), status_message, font=font, fill=WHITE)

    # Add a small line of text below the rectangle, centered horizontally with the rectangle.
    sub_message = "I'm not in my office right now. Please email me if you need anything."
    draw.text((x + (shape_width // 2) - (small_font.getbbox(sub_message)[2] // 2), top + 50 + padding), sub_message, font=small_font, fill=BLACK)

    # Add a small horizontal line underneath all that
    draw.line((x, top + 60 + small_font.getbbox(sub_message)[3], x + shape_width, top + 60 + small_font.getbbox(sub_message)[3]), fill=BLACK, width=2)

def teaching():
    ## TEACHING SIGN ##

    # Draw a rectangle.
    draw.rectangle((x, top, x + shape_width, top + 50), outline=BLACK, fill=BLACK)

    # Put text in the rectangle, centered vertically and horizontally in the rectangle.
    status_message = "Teaching a Class"
    draw.text((x + (shape_width // 2) - (font.getbbox(status_message)[2] // 2), top + (50 // 2) - (font.getbbox(status_message)[3] // 2)), status_message, font=font, fill=WHITE)

    # Add a small line of text below the rectangle, centered horizontally with the rectangle.
    sub_message = "I'm not here right now"
    draw.text((x + (shape_width // 2) - (small_font.getbbox(sub_message)[2] // 2), top + 50 + padding), sub_message, font=small_font, fill=BLACK)

    # Add a small horizontal line underneath all that
    draw.line((x, top + 60 + small_font.getbbox(sub_message)[3], x + shape_width, top + 60 + small_font.getbbox(sub_message)[3]), fill=BLACK, width=2)

def vacation():
    ## VACATION SIGN ##

    # Draw a rectangle.
    draw.rectangle((x, top, x + shape_width, top + 50), outline=BLACK, fill=BLACK)

    # Put text in the rectangle, centered vertically and horizontally in the rectangle.
    status_message = "On Vacation"
    draw.text((x + (shape_width // 2) - (font.getbbox(status_message)[2] // 2), top + (50 // 2) - (font.getbbox(status_message)[3] // 2)), status_message, font=font, fill=WHITE)

    # Add a small line of text below the rectangle, centered horizontally with the rectangle.
    sub_message = "I expect to return on [return date]. Please email me if you need anything."
    draw.text((x + (shape_width // 2) - (small_font.getbbox(sub_message)[2] // 2), top + 50 + padding), sub_message, font=small_font, fill=BLACK)

    # Add a small horizontal line underneath all that
    draw.line((x, top + 60 + small_font.getbbox(sub_message)[3], x + shape_width, top + 60 + small_font.getbbox(sub_message)[3]), fill=BLACK, width=2)

def status_bar(battery_level = 100, next_meeting_time = datetime(2026, 1, 1, 12, 0, 0)):
    # battery_level is an integer from 0 to 100 representing the percentage of battery remaining
    # next_meeting_time is a datetime object representing the time of the next free block

    # Test displaying some small status indicators in the top 10 pixels of the display

    if battery_level < 20:
        # Battery Icon
        battery_icon = Image.open("battery.png")
        battery_icon = battery_icon.resize((20, 10), Image.BICUBIC)
        image.paste(battery_icon, (1, 1))

    # Print Date in the top right corner of the display
    now = datetime.now()
    date_string = now.strftime("%B %d, %Y")
    draw.text((display.width - x_small_font.getbbox(date_string)[2] - 1, 1), date_string, font=x_small_font, fill=BLACK)

    # Bottom left corner show a list of upcoming events in a box with a title and a time for the next availability
    draw.rectangle((x + padding, display.height - 100, x + 150, display.height - 10), outline=BLACK, fill=WHITE)
    draw.text((x + padding + 5, display.height - 100), "Next Availability:", font=small_font, fill=BLACK)
    draw.text((x + padding + 5, display.height - 70), next_meeting_time.strftime("%I:%M %p"), font=small_font, fill=BLACK)

# Manually call the functions to draw the different screens -- eventually this will be done automatically after checking calendar data and getting battery status from the chip
status_bar(battery_level=15, next_meeting_time=datetime(2026, 1, 1, 14, 0, 0))

# Clunky way to select which message to show -- this will eventually be done automatically after checking calendar data

# do_not_disturb()
# available()
# working_remotely()
# out_of_office()
here_but_busy()
# office_hours()
# somewhere_else()
# teaching()
# vacation()
# in_a_meeting()


# Add an image for scheduling
overlay = Image.open("calendly_qr.png")


overlay = overlay.resize((100, 100), Image.BICUBIC)

# Paste into the lower right corner of the display
position = (display.width - overlay.width - padding, display.height - overlay.height - padding)
image.paste(overlay, position)

# Add the "Schedule a Meeting" text just to the left of the QR code
schedule_message = "Schedule\na Meeting:"
draw.text((display.width - overlay.width - padding - 20, display.height - padding - (overlay.height // 2) - 8), schedule_message, font=small_font, fill=BLACK)


display.image(image)



display.display()

print("Done!")
