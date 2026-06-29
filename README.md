# Pi Nameplate Calendar

The pi-in-the-sky idea is to use a really low-powered Pi Zero setup to drive a small eink display that I can then mount outside my office. I'd like it to read my O365 Calendar to know what my current "status" is, and use that to display an appropriate message outside my office door, such as:

- Available
- Working Remotely
- Do Not Disturb
- In a Meeting
- etc. etc.

If I leave my door open all the time, I _will_ get distracted and start yapping with anyone and everyone. But simultaneously if I keep the door shut all the time I'll get sad and lonely. Maybe this can be a happy medium


## Equipment

- Raspberry Pi Zero W
- 3.7" 416x240 Tri-Color Red / Black / White eInk - Bare Display - UC8253 Chipset (https://www.adafruit.com/product/6394)
- Adafruit E-Ink Bonnet for Raspberry Pi - 24-pin E-Paper Displays (https://www.adafruit.com/product/6418)

## Setup

[lmao I will write this eventually... maybe]

Follow Adafruit's instructions for getting stuff setup.


Install some stuff: 

- python-dotenv
- icalendar (https://icalendar.readthedocs.io/en/latest/how-to/install.html)
- requests
- tzlocal

### Environment

There are a handful of environment variables that you can set. I recommend making a `.env` file and setting them there.


| Variable Name | Required? | Default | Description |
| ------------- | ------------- | ------------- |
| DEBUG  | no | False | Display useful information for debugging and setup instead of QR code | 
| CALENDAR_URL  | yes | -- | tell the script where it can get the ICS file from |
| ICS_FILE | no | calendar.ics | what the interim ICS file should be named |
| BUSINESS_START | no | 9:30 | always be "Out of Office" prior to this time |
| BUSINESS_END | no | 4:30 | always be "Out of Office" after this time |


#### Example .env file

```
DEBUG=True
```