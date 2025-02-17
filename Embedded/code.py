# Write your code here :-)
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from neopixel import neopixel
import time
import math

#######################################################################
### change this value for each LED strip you are using on the tower ###
num_led_strips = 4
###                                                                 ###
### change this value to match the amount of LEDs per strip         ###
num_leds_per_strip = 30
#######################################################################

pixel_pin = board.GP28
num_pixels = num_led_strips*num_leds_per_strip
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER)
all_the_lights = []
for i in range(num_led_strips):
    all_the_lights.append([])
    for j in range(num_leds_per_strip):
        if i%2 == 0:
            all_the_lights[i].append(i*num_leds_per_strip+j)
        if i%2 == 1:
            all_the_lights[i].append((1+i)*num_leds_per_strip-j-1)
statuses = [False, False]
start_time = time.time()
hour = 0
count_for_lights = 0
pixels.fill((50, 20, 50))
pixels.show()

i2c=busio.I2C(board.GP21, board.GP20)
ads = ADS.ADS1115(i2c)
chan0 = AnalogIn(ads, 0)
chan1 = AnalogIn(ads, 1)

# SET AND TUNE wrt analog readings
TDS_SETPOINT = 0
WATER_SETPOINT = 0

def check_sensors():
    global statuses
    statuses = [False, False]
    
    adc0_vals = [] # TDS
    adc1_vals = [] # Water level
    for i in range(50):
        adc0_vals.append(chan0.voltage)
        adc1_vals.append(chan1.voltage)
        time.sleep(0.1) # 5 seconds spent in loop
        time.sleep(0.1) # 5 seconds spent in loop
    adc0_mean = sum(adc0_vals) / len(adc0_vals)
    adc1_mean = sum(adc1_vals) / len(adc1_vals)
    if adc0_mean > TDS_SETPOINT: # the TDS sensor is below threshold
        statuses[0] = True
    if adc1_mean > WATER_SETPOINT: # the water level sensor is below threshold
        statuses[1] = True

def handle_lights():
    global count_for_lights
    global pixels
    global all_the_lights
    pixels.fill((50, 20, 50))
    water_light = (20, 180, 255)
    tds_light = (255, 180, 20)
    for i in range(len(all_the_lights)): #for each led strip
        for j in range(len(all_the_lights[0])): #for all lights in a strip
            if statuses[0] & statuses[1]: # if both sensors are below threshold
                if j % 6 == abs(4-(count_for_lights % 10)):
                    if count_for_lights % 10 >= 5:
                        pixels[all_the_lights[i][j]] = tds_light
                    else:
                        pixels[all_the_lights[i][j]] = water_light
            elif statuses[0]: # if only TDs
                if j % 6 == count_for_lights % 6:
                    pixels[all_the_lights[i][j]] = tds_light
            elif statuses[1]: # if only water
                if j % 6 == 5 - count_for_lights % 6:
                    pixels[all_the_lights[i][j]] = water_light
    count_for_lights += 1
    count_for_lights %= 30
    pixels.show()

while True :
    if ((time.time()-start_time) // 3600) % 24 != hour: 
        hour = ((time.time()-start_time) // 3600) % 24 
        if hour >= 12:
            pixels.fill((0, 0, 0))
            pixels.show()
            time.sleep(43210) # sleep for 12 hours if the time is 12 hours after start
        else:
            pixels.fill((50, 20, 50))
            pixels.show() # clear the alerts incase there are none
            check_sensors()

    if statuses[0] or statuses[1]:
        handle_lights()
    elif (time.time()-start_time) % 3600 < 100:
        time.sleep(3450)
    time.sleep(.15)