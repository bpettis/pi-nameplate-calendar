from gpiozero import Button

button_5 = Button(5)
button_6 = Button(6)

while True:
    if button_5.is_pressed:
        print("Button 5 is pressed")
        with open('/sys/class/leds/ACT/brightness', 'w') as f:
            f.write('1')
    else:
        with open('/sys/class/leds/ACT/brightness', 'w') as f:
            f.write('0')

    if button_6.is_pressed:
        print("Button 6 is pressed")
        with open('/sys/class/leds/ACT/brightness', 'w') as f:
            f.write('1')
    else:
        with open('/sys/class/leds/ACT/brightness', 'w') as f:
            f.write('0')