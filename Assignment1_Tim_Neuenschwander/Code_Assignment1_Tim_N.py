
#!/usr/bin/python

import RPi.GPIO as GPIO
from datetime import datetime
from time import sleep
import os
from rpi_ws281x import *
import time
from random import randrange

############
# CONSTANTS#
############
# Input pin is 15 (GPIO22)
INPUT_PIN = 15
# To turn on debug print outs, set to 1
DEBUG = 1

###################
# INITIALIZE PINS #
###################
GPIO.setmode(GPIO.BOARD)
GPIO.setup(INPUT_PIN, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(INPUT_PIN, GPIO.IN)

# LED strip configuration:
LED_COUNT      = 1      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        



# Main loop, listen for infinite packets
while True:
    print("\nWaiting for GPIO low")

    # If there was a transmission, wait until it finishes
    #GPIO.wait_for_edge(INPUT_PIN, GPIO.RISING)
    value = 1
    while value:
        sleep(0.001)
        #print("Last read value: {}".format(value))
        value = GPIO.input(INPUT_PIN)       

    # timestamps for pulses and packet reception
    startTimePulse = datetime.now()
    previousPacketTime = 0

    print("\nListening for an IR packet")

    # Buffers the pulse value and time durations
    pulseValues = []
    timeValues = []

    # Variable used to keep track of state transitions
    previousVal = 0

    # Inner loop 
    while True:
        # Measure time up state change
        if value != previousVal:
            # The value has changed, so calculate the length of this run
            now = datetime.now()
            pulseLength = now - startTimePulse
            startTimePulse = now

            # Record value and duration of current state
            pulseValues.append(value)
            timeValues.append(pulseLength.microseconds)
            
            # Detect short IR packet using packet length and special timing
            if(len(pulseValues) == 3):
                if(timeValues[1] < 3000):
                    print("Detected Short IR packet")
                    print(pulseValues)
                    print(timeValues)
                    break;

            # Detect standard IR packet using packet length 
            if(len(pulseValues) == 67):
                if(DEBUG==1):
                    print("Finished receiving standard IR packet")
                    print(pulseValues)
                    print(timeValues)
                    
                    #Tim's code
                    
                    address1 = timeValues[2:18]
                    address2 = timeValues[18:34]
                    message1 = timeValues[34:50]
                    message2 = timeValues[50:66]
                    print("")
                    print("This is A1:", address1)
                    print("This is A2:", address2)
                    print("This is M1:", message1)
                    print("This is M2:", message2)
                    print("")
                    
                    del address1[::2]
                    a1 = list(map(int, address1))
                    print(a1)
                    
                    del address2[::2]
                    a2 = list(map(int, address2))
                    print(a2)
                    
                    del message1[::2]
                    m1 = list(map(int, message1))
                    print(m1)
                    
                    del message2[::2]
                    m2 = list(map(int, message2))
                    print(m2)
                    
                    button = []
                    for i in m1:
                        if i > 1000:
                            button.append(1)
                        else:
                            button.append(0)
                    print("This is the button you pushed:",button)
                    
                    buttonneg = []
                    for i in m2:
                        if i > 1000:
                            buttonneg.append(1)
                        else:
                            buttonneg.append(0)
                    print("This is the negative of the button you pushed:", buttonneg)
                    
                    
                    
                    #Nr 1-3
                    if button == [1, 0, 1, 0, 0, 0, 1, 0]:
                        print("Button number 1")
                    elif button == [0, 1, 1, 0, 0, 0, 1, 0]:
                        print("Button number 2")
                    elif button == [1, 1, 1, 0, 0, 0, 1, 0]:
                        print("Button number 3")
                    
                    #Nr 4-6
                    elif button == [0, 0, 1, 0, 0, 0, 1, 0]:
                        print("Button number 4")
                    elif button == [0, 0, 0, 0, 0, 0, 1, 0]:
                        print("Button number 5")
                    elif button == [1, 1, 0, 0, 0, 0, 1, 0]:
                        print("Button number 6")
                    
                    #Nr 7-9
                    elif button == [1, 1, 1, 0, 0, 0, 0, 0]:
                        print("Button number 7")         
                    elif button == [1, 0, 1, 0, 1, 0, 0, 0]:
                        print("Button number 8")
                    elif button == [1, 0, 0, 1, 0, 0, 0, 0]:
                        print("Button number 9")
                    
                    #Nr 0+OK
                    elif button == [1, 0, 0, 1, 1, 0, 0, 0]:
                        print("Button number 0")
                        colorWipe(strip, Color(0, 0, 0))
                    
                    elif button == [0, 0, 1, 1, 1, 0, 0, 0]:
                        print("Button = OK")
                        colorWipe(strip, Color(0, 255, 0))
                        
                    #Arrows
                        
                        #Switch colour
                    elif button == [0, 1, 0, 1, 1, 0, 1, 0]:
                        print("Button Arrow right")
                        print("Switch Colour random")
                        a = randrange(255)
                        print (a)
                        b = randrange(255)
                        print (b)
                        c = randrange(255)
                        print (c)
                        colorWipe(strip, Color(a, b, c))
                    elif button == [0, 0, 0, 1, 0, 0, 0, 0]:
                        print("Button Arrow left")
                        print("Switch Colour random")
                        a = randrange(255)
                        print (a)
                        b = randrange(255)
                        print (b)
                        c = randrange(255)
                        print (c)
                        colorWipe(strip, Color(a, b, c))
                        
                        #Dim light
                    elif button == [0, 0, 0, 1, 1, 0, 0, 0]:
                        print("Button Arrow up")
                        
                        if a + 30 < 255:
                            a = a + 30
                        if b + 30 < 255:
                            b = b + 30    
                        if c + 30 < 255:
                            c = c + 30
                            
                        print (a)
                        print (b)
                        print (c)
                        
                        if a + b + c < 765:
                            colorWipe(strip, Color(a, b, c))
                            
                        """
approach 2:
                        if a + 30 < 255 and b + 30 < 255 and c + 30 < 255: 
                            a = a + 30
                            b = b + 30
                            c = c + 30
                            
                        print (a)
                        print (b)
                        print (c)
                        
                        if a + b + c < 765:
                            colorWipe(strip, Color(a, b, c))
                        """
                            
                    elif button == [0, 1, 0, 0, 1, 0, 1, 0]:
                        print("Button Arrow down")
                        
                        if a - 30 > 0:
                            a = a - 30   
                        if b - 30 > 0:
                            b = b - 30   
                        if c - 30 > 0:
                            c = c - 30
                            
                        print (a)
                        print (b)
                        print (c)
                        
                        if a + b + c > 0:
                            colorWipe(strip, Color(a, b, c))
                        
                        """
approach 2:
                        if a - 30 > 0 and b - 30 > 0 and c - 3> 0: 
                            a = a - 30
                            b = b - 30
                            c = c - 30
                            
                        print (a)
                        print (b)
                        print (c)
                        
                        if a + b + c > 0:
                            colorWipe(strip, Color(a, b, c))
                        """
                    else:
                        print("Please press button again :)")
                    
                    #TODO: Decode packet and perform task
                    break;

        # save state
        previousVal = value
        # read GPIO pin
        value = GPIO.input(INPUT_PIN)


