import plasma
import utime
import time
import random

from plasma import plasma_stick
from machine import Pin

# Set how many LEDs you have
NUM_LEDS = 100

# Pick two hues from the colour wheel (from 0-360°, try https://www.cssscript.com/demo/hsv-hsl-color-wheel-picker-reinvented/ )
HUE_1 = 40
HUE_2 = 285

BRIGHTNESS = 0.8 # Set up brightness (between 0 and 1)
SPEED = 1 # Set up speed (wait time between colour changes, in seconds)
UPDATES = 60 # How many times the LEDs will be updated per second
SWITCH = 10 # Number of times to switch colours

led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma_stick.DAT, color_order=plasma.COLOR_ORDER_RGB) # WS2812 / NeoPixel™ LEDs
led_strip.start() # Start updating the LED strip
button = Pin(16, Pin.IN, Pin.PULL_UP) # Momentary button on GPIO pin 16

offset = 0.0

# Sample Raspberry Pi Pico MicroPython button press example with a debounce delay value of 200ms in the interrupt handler
button_presses = 1 # the count of times the button has been pressed
last_time = 0 # the last time we pressed the button

builtin_led = machine.Pin(25, Pin.OUT)
# the lower left corner of the Pico has a wire that goes through the buttons upper left and the lower right goes to the 3.3 rail
button_pin = Pin(16, Pin.IN, Pin.PULL_UP) # Momentary button on GPIO pin 16

# this function gets called every time the button is pressed
def button_pressed_handler(pin):
    global button_presses, last_time
    new_time = utime.ticks_ms()
    # if it has been more that 1/5 of a second since the last event, we have a new event
    if (new_time - last_time) > 200: 
        button_presses +=1
        last_time = new_time

def ambient(sat, spd): # Pale coloured rainbows
    global NUM_LEDS, HUE_1, HUE_2, BRIGHTNESS, UPDATES, led_strip, offset
    SPEED = 2 # Set up speed (wait time between colour changes, in seconds)
    SPEED = min(255, max(1, spd))
    BRIGHTNESS = 0.6
    offset += float(SPEED) / 2000.0

    for i in range(NUM_LEDS):
        hue = float(i) / NUM_LEDS
        led_strip.set_hsv(i, hue + offset, sat, BRIGHTNESS)

    time.sleep(1.0 / UPDATES)
    
def solid(sat, spd): # Pale coloured rainbows
    global NUM_LEDS, HUE_1, HUE_2, BRIGHTNESS, UPDATES, led_strip, offset
    SPEED = 2 # Set up speed (wait time between colour changes, in seconds)
    SPEED = min(255, max(1, spd))
    BRIGHTNESS = 0.6
    offset += float(SPEED) / 2000.0

    for i in range(NUM_LEDS):
        hue = float(i) / NUM_LEDS
        led_strip.set_hsv(i, 1 + offset, sat, BRIGHTNESS)

    time.sleep(1.0 / UPDATES)
        
        
# now we register the handler function when the button is pressed
button_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler = button_pressed_handler)

# This is for only printing when a new button press count value happens
old_presses = 0
while True:
    # only print on change in the button_presses value
    if button_presses != old_presses:
        print(button_presses)
        old_presses = button_presses
    
    # Change the state of the LEDs based on sequence of button presses. Cycle back to start on end of range
    if button_presses == 1:
        ambient(0.2, 15)
    if button_presses == 2:
        ambient(0.3, 13)
    if button_presses == 3:
        ambient(0.4, 10)
    if button_presses == 4:
        ambient(0.5, 4)
    if button_presses == 5:
        ambient(1.0, 2)
    if button_presses == 6:
        ambient(1.0, 20)
    if button_presses == 7:
        solid(1.0, 1)
    if button_presses == 8:
        ambient(0.1, 20)
    if button_presses == 9:
        button_presses = 1
