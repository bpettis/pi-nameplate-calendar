import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 5 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 5 to be an input pin and set initial value to be pulled low (off)

# Run forever:
while True:
    if GPIO.input(5) == GPIO.HIGH:
        print("Button 5 was pushed!")

    if GPIO.input(6) == GPIO.HIGH:
        print("Button 6 was pushed!")

# with open('/sys/class/leds/ACT/brightness', 'w') as f:
#     f.write('1')
    
# with open('/sys/class/leds/ACT/brightness', 'w') as f:
#     f.write('0')