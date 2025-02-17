# Write your code here :-)
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from neopixel import neopixel
import time
import math

pixel_pin = board.GP28
num_pixels = 120
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER)
all_the_lights = [
 [[0, 1, 2, 3, 4, 5], [59, 58, 57, 56, 55, 54], [60, 61, 62, 63, 64, 65], [119, 118, 117, 116, 115, 114]],
 [[6, 7, 8, 9, 10, 11], [53, 52, 51, 50, 49, 48], [66, 67, 68, 69, 70, 71], [113, 112, 111, 110, 109, 108]],
 [[12, 13, 14, 15, 16, 17], [47, 46, 45, 44, 43, 42], [72, 73, 74, 75, 76, 77], [107, 106, 105, 104, 103, 102]],
 [[18, 19, 20, 21, 22, 23], [41, 40, 39, 38, 37, 36], [78, 79, 80, 81, 82, 83], [101, 100, 99, 98, 97, 96]],
 [[24, 25, 26, 27, 28, 29], [35, 34, 33, 32, 31, 30], [84, 85, 86, 87, 88, 89], [95, 94, 93, 92, 91, 90]]
]
statuses = [False, False]
start_time = time.time()
hour = 0
count_for_lights = 0
pixels.fill((50, 20, 50))
pixels.show()
count = 0

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
    for i in range(5): # check each rowlayer
        if statuses[0] & statuses[1]: # if both
            for j in range(4):
                if count_for_lights % 10 >= 5:
                    pixels[all_the_lights[i][j][abs(4-(count_for_lights % 10))]] = tds_light
                else:
                    pixels[all_the_lights[i][j][abs(4-(count_for_lights % 10))]] = water_light
        elif statuses[0]: # if only TDS
            for j in range(4):
                pixels[all_the_lights[i][j][count_for_lights%6]] = tds_light
        elif statuses[1]: # if only water
            for j in range(4):
                pixels[all_the_lights[i][j][5-count_for_lights%6]] = water_light
    count_for_lights += 1
    if count_for_lights == 30:
        count_for_lights = 0
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
