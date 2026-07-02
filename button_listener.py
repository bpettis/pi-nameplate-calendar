from gpiozero import Button
import time
from display_update import main as update_display
from pathlib import Path
from download_calendar import main as download_calendar

button_5 = Button(5)
button_6 = Button(6)

print("Button listener started. Waiting for button presses...")
while True:
    if button_5.is_pressed:
        print("Button 5 is pressed")
        with open('/sys/class/leds/ACT/brightness', 'w') as f:
            f.write('1')
        time.sleep(0.5)  # Debounce delay
        
        # Check if manual_dnd file exists
        manual_dnd_path = Path("manual_dnd_mode")
        if manual_dnd_path.exists():
            print("Manual DND file exists. Removing it...")
            time.sleep(0.5)
            manual_dnd_path.unlink()  # Remove the file
            update_display()
        else:
            print("Manual DND file does not exist. Creating it...")
            manual_dnd_path.touch()  # Create the file
            time.sleep(0.5)
            update_display()
        
        with open('/sys/class/leds/ACT/brightness', 'w') as f:
            f.write('0')
        print("Finished processing")

    if button_6.is_pressed:
        print("Button 6 is pressed")
        print("Downloading calendar and updating display...")
        with open('/sys/class/leds/ACT/brightness', 'w') as f:
            f.write('1')
        time.sleep(0.5)  # Debounce delay
        download_calendar()
        update_display()
        with open('/sys/class/leds/ACT/brightness', 'w') as f:
            f.write('0')
        print("Finished processing")