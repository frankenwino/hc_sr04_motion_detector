# -*- coding: utf-8 -*-

"""Main module."""

"""
1. Plug four of your male to female jumper wires into the pins on the HC-SR04 as follows:
    Red; Vcc, Blue; GPIO_TRIGGER, Yellow; GPIO_ECHO and Black; GND.
2. Plug Vcc into the positive rail of your breadboard, and plug GND into your negative rail.
3. Plug GPIO 5V [Pin 2] into the positive rail, and GPIO GND [Pin 6] into the negative rail.
    See: https://github.com/frankenwino/hc_sr04_activated_28byj_48/raw/master/hc_sr04_activated_28byj_48/images/3.%20hc-sr04-tut-4_1024x1024.jpg
4. Plug GPIO_TRIGGER into a blank rail, and plug that rail into GPIO 23 [Pin 16]. (You can plug GPIO_TRIGGER directly into GPIO 23 if you want).
    See: https://github.com/frankenwino/hc_sr04_activated_28byj_48/raw/master/hc_sr04_activated_28byj_48/images/4.%20hc-sr04-tut-5_1024x1024.jpg
5. Plug GPIO_ECHO into a blank rail, link another blank rail using R1 (1kΩ resistor)
6. Link your R1 rail with the GND rail using R2 (2kΩ resistor). Leave a space between the two resistors.
    See: https://github.com/frankenwino/hc_sr04_activated_28byj_48/raw/master/hc_sr04_activated_28byj_48/images/6.%20hc-sr04-tut-6_1024x1024.jpg
7. Add GPIO 24 [Pin 18] to the rail with your R1 (1kΩ resistor). This GPIO pin needs to sit between R1 and R2

That's it! The HC-SR04 sensor is connected to our Raspberry Pi!
    See: https://github.com/frankenwino/hc_sr04_activated_28byj_48/raw/master/hc_sr04_activated_28byj_48/images/8.%20hc-sr04-tut-8_1024x1024.jpg
"""

import RPi.GPIO as GPIO
import time
from datetime import datetime


def right_now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def print_message(the_message):
    print("{} - {}".format(right_now(), the_message))


def measure_distance():
    # Measures the distance from the HR-SR04 sensor
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        pulse_stop = time.time()

    pulse_duration = pulse_stop - pulse_start
    distance = (pulse_duration * 34300)/2
    distance = round(distance, 2)

    return distance


GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 23
GPIO_ECHO = 24

# Set pins as output and input
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)   # Trigger
GPIO.setup(GPIO_ECHO, GPIO.IN)       # Echo

# Set trigger to False (Low)
GPIO.output(GPIO_TRIGGER, False)


distance_trigger = 30  # centimetres
wait_after_detection_seconds = 2

if __name__ == '__main__':
    print_message(the_message="HC-SR04 ultrasonic distance measurement")
    print_message(the_message="Waiting for HC-SR04 sensor to settle")
    time.sleep(2)
    print_message(
    the_message="System will trigger when HC-SR04 sensor detects something {} cm away".format(distance_trigger))

    try:
        while True:
            distance = measure_distance()
            message = "Nearest thing is {} cm away".format(distance)
            print_message(the_message=message)

            if distance < distance_trigger:
                print_message("Something detected {} cm away".format(distance))
                # Do something here
                print_message(
                    the_message="Waiting {} seconds before re-starting HC-SR04 sensor".format(wait_after_detection_seconds))
                time.sleep(wait_after_detection_seconds)
                print_message(
                    the_message="System will GPIO_TRIGGERger when HC-SR04 sensor detects something {} cm away".format(distance_trigger))

            else:
                time.sleep(0.5)
    except KeyboardInterrupt:  # User pressed CTRL-C
        # Reset GPIO settings
        GPIO.cleanup()

