# SPDX-FileCopyrightText: 2019 Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
ePaper Display Shapes and Text demo using the Pillow Library.

"""
print("Started!")

import board
import busio
import digitalio
import os
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.epd import Adafruit_EPD
from datetime import datetime
from dotenv import load_dotenv
from adafruit_epd.uc8253 import Adafruit_UC8253_Tricolor
from current_event import main as get_calendar_data

print("Finished Imports")

# Load Environment Variables
load_dotenv()
DEBUG = True if (os.getenv("DEBUG") == "True") else False
BUSINESS_START = datetime.strptime(os.getenv("BUSINESS_START", "09:30"), "%H:%M").time()
BUSINESS_END = datetime.strptime(os.getenv("BUSINESS_END", "16:30"), "%H:%M").time()

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
lbo = digitalio.DigitalInOut(board.D4)

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
# Move left to right keeping track of the current x position for drawing shapes.
x = padding


# Load default font.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
med_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
x_small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
print("Finished setting up display and fonts")



def display_message(status_message = "[MESSAGE HERE]", sub_message = "[SUB MESSAGE HERE]", box_color = BLACK, text_color = WHITE):
    # Draw a rectangle.
    draw.rectangle((x, top, x + shape_width, top + 50), outline=box_color, fill=box_color)

    # Put text in the rectangle, centered vertically and horizontally in the rectangle.
    draw.text((x + (shape_width // 2) - (font.getbbox(status_message)[2] // 2), top + (50 // 2) - (font.getbbox(status_message)[3] // 2)), status_message, font=font, fill=text_color)

    # Add a small line of text below the rectangle, centered horizontally with the rectangle.
    draw.text((x + (shape_width // 2) - (small_font.getbbox(sub_message)[2] // 2), top + 50 + padding), sub_message, font=small_font, fill=BLACK)

    # Add a small horizontal line underneath all that
    draw.line((x, top + 60 + small_font.getbbox(sub_message)[3], x + shape_width, top + 60 + small_font.getbbox(sub_message)[3]), fill=BLACK, width=2)

def status_bar(battery_ok = True, next_meeting_time = [(datetime(2026, 1, 1, 12, 0, 0), datetime(2026, 1, 1, 13, 0, 0))]):
    # battery_ok is a boolean representing whether the battery level is ok -- the lbo pin gets pulled low when the chip detects a low voltage, which we'll read as a low battery
    # next_meeting_time is an array of tuples of datetime objects representing the start and end time of the next free block

    # Test displaying some small status indicators in the top 10 pixels of the display

    if not battery_ok:
        # Battery Icon
        battery_icon = Image.open("battery.png")
        battery_icon = battery_icon.resize((20, 10), Image.BICUBIC)
        image.paste(battery_icon, (1, 1))

    # Print Date in the top right corner of the display
    now = datetime.now()
    date_string = now.strftime("%A, %B %-d, %Y")
    draw.text((display.width - x_small_font.getbbox(date_string)[2] - 1, 1), date_string, font=x_small_font, fill=BLACK)

    # Bottom left corner show a list of upcoming events in a box with a title and a time for the next availability
    draw.rectangle((x + padding, display.height - 100, x + 175, display.height - 10), outline=BLACK, fill=WHITE)
    draw.text((x + padding + 5, display.height - 100), "Upcoming Availability:", font=small_font, fill=BLACK)

    # break if the next_meeting_time array is empty
    if len(next_meeting_time) == 0:
        draw.text((x + padding + 5, display.height - 80), "-- none --", font=small_font, fill=BLACK)
        draw.text((x + padding + 5, display.height - 68), "Use the QR code to\nschedule a\nmeeting.", font=small_font, fill=BLACK)
        return

    for i in range(len(next_meeting_time)):
        draw.text((x + padding + 5, display.height - 80 + (i * 14)), next_meeting_time[i][0].strftime("%-I:%M %p - %a %b %-d"), font=small_font, fill=BLACK)
        if i >= 4:
            break


def main():

    # Get calendar data
    try:
        current_events, free_windows = get_calendar_data()
    except Exception as e:
        print(f"Failed to get calendar data: {e}")
        current_events = []
        free_windows = []

    # Manually call the functions to draw the different screens

    upcoming_meetings = free_windows
    print(f"Battery OK: {lbo.value}")
    status_bar(battery_ok=lbo.value, next_meeting_time=upcoming_meetings)

    # Clunky way to select which message to show -- this will eventually be done automatically after checking calendar data


    ''' ### Messages and Color Pairings, and sub-messages ###
    Eventually we'll select these based on calendar data -- possibly reading from some other file that is updated by a separate script.

    Do Not Disturb: Red Box, White Text, I will yap and yap if given the opportunity...
    In a Meeting: Red Box, Black Text, Please do not disturb me unless it's an emergency.
    Available: Black Box, White Text, Feel free to stop by and chat!
    Working Remotely: Black Box, White Text, Please email me if you need anything.
    Out of Office: Black Box, White Text, I may have limited access to email, but I will respond as soon as I can.
    Here, But Busy: Black Box, White Text, Please knock only if it's urgent.
    Office Hours: Black Box, White Text, Come on in! I'm here to help.
    Somewhere Else: Black Box, Red Text, I'm not in my office right now. Please email me if you need anything.
    Teaching a Class: Black Box, Red Text, I'm not here right now
    On Vacation: Black Box, White Text, I expect to return on [return date]. Please email me if you need anything.

    '''

    state = ""


    if current_events:
        print("Current events:\n")
        for event, start, end in current_events:
            print(event)
            print("Summary:", event.get("summary"))
            print("Location:", event.get("location"))
            print("Description:", event.get("description"))
            print("-" * 40)

            # Check the event title to see if it contains a matching string that should always be matched to a specific state
            # For example, anything that starts with "Writing Time:" should always be matched to "Do Not Disturb" regardless of the other data in the event.
            # Or anything that is labelled as "Office Hours" should always be matched to "Office Hours" regardless of the other data in the event.
            # Anything labelled as "Vacation" should always be matched to "On Vacation" regardless of the other data in the event.
            # Anything labelled with "RHCS:" should match to "Teaching a Class" regardless of the other data in the event.
            title = event.get("summary", "").lower()
            if title.startswith("writing time:"):
                state = "Do Not Disturb"
            elif title.startswith("office hours"):
                state = "Office Hours"
            elif title.startswith("vacation"):
                state = "On Vacation"
            elif title.startswith("rhcs"):
                state = "Teaching a Class"
            elif title.startswith("working remotely"):
                state = "Working Remotely"


            # Check the event location to see if it contains a matching string that should always be matched to a specific state
            # For example, if there is an address in the location field that is not "my office," "ben's office", or "Weinstein 402G" or "Jepson 221", then we should display "Somewhere Else" regardless of the other data in the event.
            location = event.get("location", "").lower()
            if location and "my office" not in location and "ben's office" not in location and "weinstein 402g" not in location and "jepson 221" not in location:
                state = "Somewhere Else"

            # Check the event description for a custom string to specify the state to display on the nameplate. If found, use that string as the state.
            # This should be the top priority for determining the state, as it allows for manual override of the calendar data. The format should be "## NAMEPLATE_STATE: [STATE] ##" where [STATE] is one of the states listed above.
            # For example ## NAMEPLATE_STATE: Available ## would set the state to "Available" and display the appropriate message and colors on the nameplate.
            description = event.get("description", "").lower()
            if "## NAMEPLATE_STATE:" in description:
                state_line = [line for line in description.splitlines() if "## NAMEPLATE_STATE:" in line][0]
                state = state_line.split("## NAMEPLATE_STATE:") [1].strip()

            

            # TO-DO: Check if I am working in person or remotely, and display the appropriate message. For now, just display "In a Meeting"
    else:
        print("No events are currently in progress.")
        state = "Available"


        # Check if we are outside of business hours (default 9:30 AM to 4:30 PM) and if so, display "Out of Office" regardless of the calendar data.
        now = datetime.now()
        if now.time() < BUSINESS_START or now.time() > BUSINESS_END:
            state = "Out of Office"
        # TO-DO: Check if I am working in person or remotely, and display the appropriate message. For now, just display "Available"
        



    match state:
        case "Available":
            display_message(status_message="Available", sub_message="Feel free to stop by and chat!", box_color=BLACK, text_color=WHITE)
        case "In a Meeting":
            display_message(status_message="In a Meeting", sub_message="Please do not disturb me unless it's an emergency.", box_color=RED, text_color=BLACK)
        case "Do Not Disturb":
            display_message(status_message="Do Not Disturb", sub_message="I will yap and yap if given the opportunity...", box_color=RED, text_color=WHITE)
        case "Working Remotely":
            display_message(status_message="Working Remotely", sub_message="Please email me if you need anything.", box_color=BLACK, text_color=WHITE)
        case "Out of Office":
            display_message(status_message="Out of Office", sub_message="Limited access to email, but I will respond as soon as I can.", box_color=BLACK, text_color=WHITE)
        case "Here, But Busy":
            display_message(status_message="Here, But Busy", sub_message="Please knock only if it's urgent.", box_color=BLACK, text_color=WHITE)
        case "Office Hours":
            display_message(status_message="Office Hours", sub_message="Come on in! I'm here to help.", box_color=BLACK, text_color=WHITE)
        case "Somewhere Else":
            display_message(status_message="Somewhere Else", sub_message="I'm not in my office right now. Please email me if you need anything.", box_color=BLACK, text_color=RED)
        case "Teaching a Class":
            display_message(status_message="Teaching a Class", sub_message="I'm not here right now.", box_color=BLACK, text_color=RED)
        case "On Vacation":
            display_message(status_message="On Vacation", sub_message="I am happy to meet when I return. Please email me if you need anything.", box_color=BLACK, text_color=WHITE)
        case _:
            display_message(status_message="???", sub_message="I've lost my marbles (and may or may not be around)", box_color=BLACK, text_color=WHITE)

    print(f'State: {state}')

    if DEBUG:
        print("Debug mode is on. Skipping QR code.")
        uptime = os.popen('uptime -p').read()[:-1]
        ssid = os.popen('iwgetid -r').read()[:-1]
        ip = os.popen('hostname -I').read()[:-1]
        mac = os.popen('cat /sys/class/net/wlan0/address').read()[:-1]

        timestamp = 'unknown'
        with open("last_download", "r") as f:
            timestamp = f.read()

        draw.text((display.width // 2 - ( padding // 2), display.height // 2 + 0), uptime, font=small_font, fill=BLACK)
        draw.text((display.width // 2 - ( padding // 2), display.height // 2 + 12), f'Last Run:', font=small_font, fill=BLACK)
        draw.text((display.width // 2 - ( padding // 2), display.height // 2 + 24), f'    {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', font=small_font, fill=BLACK)
        draw.text((display.width // 2 - ( padding // 2), display.height // 2 + 36), f'WiFi: {ssid}', font=small_font, fill=BLACK)
        draw.text((display.width // 2 - ( padding // 2), display.height // 2 + 48), f'MAC: {mac}', font=small_font, fill=BLACK)
        draw.text((display.width // 2 - ( padding // 2), display.height // 2 + 60), f'IP: {ip}', font=small_font, fill=BLACK)
        draw.text((display.width // 2 - ( padding // 2), display.height // 2 + 72), f'Battery OK: {lbo.value}', font=small_font, fill=BLACK)
        draw.text((display.width // 2 - ( padding // 2), display.height // 2 + 84), f'Calendar Refreshed:', font=small_font, fill=BLACK)
        draw.text((display.width // 2 - ( padding // 2), display.height // 2 + 96), f'    {timestamp}', font=small_font, fill=BLACK)

    else:
        # Add an image for scheduling
        overlay = Image.open("calendly_qr.png")


        overlay = overlay.resize((100, 100), Image.BICUBIC)

        # Paste into the lower right corner of the display
        position = (display.width - overlay.width - padding, display.height - overlay.height - padding)
        image.paste(overlay, position)

        # Add the "Schedule a Meeting" text just to the left of the QR code
        schedule_message = "Schedule\na Meeting:"
        draw.text((display.width - ( 2 * overlay.width) - ( padding // 2), display.height - padding - (overlay.height // 2) - 8), schedule_message, font=small_font, fill=BLACK)

    

    # Finally, send the image to the display hardware to be shown
    display.image(image)

    # Tell the display to refresh
    display.display()

    

if __name__ == '__main__':
    print("Starting main()...")
    with open('/sys/class/leds/ACT/brightness', 'w') as f:
        f.write('1')
    main()
    with open('/sys/class/leds/ACT/brightness', 'w') as f:
        f.write('0')
    print("Done!")