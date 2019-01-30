from phue import Bridge
import math
import sys
import re
import time

""" ################ """
""" general settings """
""" ################ """

# Windows Home
sys.path.insert(0, "C:/Users/stanman/Desktop/Unterlagen/GIT/Python_Projects/RasPi/SmartHome/led/")

# Windows Work
#sys.path.insert(0, "C:/Users/mstan/GIT/Python_Projects/RasPi/SmartHome/led")

# RasPi:
#sys.path.insert(0, "/home/pi/Python/SmartHome/led")


""" ################# """
""" support functions """
""" ################# """

# This is based on original code from http://stackoverflow.com/a/22649803

def EnhanceColor(normalized):
    if normalized > 0.04045:
        return math.pow( (normalized + 0.055) / (1.0 + 0.055), 2.4)
    else:
        return normalized / 12.92

def RGBtoXY(r, g, b):
    rNorm = r / 255.0
    gNorm = g / 255.0
    bNorm = b / 255.0

    rFinal = EnhanceColor(rNorm)
    gFinal = EnhanceColor(gNorm)
    bFinal = EnhanceColor(bNorm)
    
    X = rFinal * 0.649926 + gFinal * 0.103455 + bFinal * 0.197109
    Y = rFinal * 0.234327 + gFinal * 0.743075 + bFinal * 0.022598
    Z = rFinal * 0.000000 + gFinal * 0.053077 + bFinal * 1.035763

    if X + Y + Z == 0:
        return (0,0)
    else:
        xFinal = X / (X + Y + Z)
        yFinal = Y / (X + Y + Z)
    
    return (xFinal, yFinal)


def CONNECT_BRIDGE():
    from LED_database import GET_BRIDGE_IP
    b = Bridge(GET_BRIDGE_IP())
    b.connect() 
    return b       


def GET_LED_NAME():
    b = CONNECT_BRIDGE()
    lights = b.get_light_objects('list')

    light_list = []
    for light in lights:
        light_list.append(light.name)
    
    return light_list


""" ############# """
""" LED functions """
""" ############# """

def LED_SET_SCENE(scene, brightness_global = 100):
    b = CONNECT_BRIDGE()
    lights = b.get_light_objects('list')
    # deactivate all LED
    for light in lights:
        light.on = False

    from LED_database import GET_SCENE

    # get scene settings
    entries = GET_SCENE(scene)
    if entries[0] is not None:
        entries = entries[0]
        for entry in entries:
                # set rgb 
                xy = RGBtoXY(entry.color_red, entry.color_green, entry.color_blue)
                lights[entry.LED_id - 1].on = True
                lights[entry.LED_id - 1].xy = xy
             
                # set brightness
                brightness = entry.brightness
                # add global brightness setting
                brightness = int(brightness * (int(brightness_global) / 100))
                if brightness > 10:
                    lights[entry.LED_id - 1].brightness = brightness
                else:
                    # turn LED off if brightness < 10
                    lights[entry.LED_id - 1].on = False               


""" ################# """
""" program functions """
""" ################# """

def PROGRAM_SET_BRIGHTNESS(brightness_settings):
    b = CONNECT_BRIDGE()
    lights = b.get_light_objects('list')
  
    brightness_settings = brightness_settings.split(":")
    # get the brightness value only (source: bri(xxx))
    brightness = re.findall(r'\d+', brightness_settings[1]) 
    # transform list element to int   
    brightness = int(brightness[0])
    if brightness > 10:
            # list element start at 0 for LED ID 1
            lights[int(brightness_settings[0]) - 1].on = True
            lights[int(brightness_settings[0]) - 1].brightness = brightness
    else:
            # turn LED off if brightness < 10
            lights[int(brightness_settings[0]) - 1].on = False               


def PROGRAM_SET_COLOR(rgb_settings):
    b = CONNECT_BRIDGE()
    lights = b.get_light_objects('list')

    rgb_settings = rgb_settings.split(":")
    # get the rgb values only (source: rgb(xxx, xxx, xxx))
    rgb_color = re.findall(r'\d+', rgb_settings[1])     
    # convert rgb to xy    
    xy = RGBtoXY(int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2]))
    lights[int(rgb_settings[0]) - 1].on = True
    lights[int(rgb_settings[0]) - 1].xy = xy


def START_PROGRAM(id):  
    b = CONNECT_BRIDGE()
    lights = b.get_light_objects('list')
    # deactivate all LED
    for light in lights:
        light.on = False

    from LED_database import GET_PROGRAM_ID
    content = GET_PROGRAM_ID(id).content

    try:   
        # select each command line
        for line in content.splitlines():
            if "rgb" in line: 
                PROGRAM_SET_COLOR(line)
            if "bri" in line: 
                PROGRAM_SET_BRIGHTNESS(line)
            if "pause" in line: 
                break_value = line.split(":")
                break_value = int(break_value[1])
                time.sleep(break_value)
    except:
        pass

    return True