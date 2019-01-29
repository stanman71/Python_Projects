from phue import Bridge
import math
import sys
import re

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

def LED_SET_BRIGHTNESS(brightness):
    b = CONNECT_BRIDGE()
    lights = b.get_light_objects('list')
    
    # set brightness
    for i in range(len(brightness)):
        if brightness[i] is not None:
            if int(brightness[i]) > 10:
                    lights[i].on = True
                    lights[i].brightness = int(brightness[i])
            # turn LED off if brightness < 10
            else:
                    lights[i].on = False               


def LED_SET_COLOR(rgb_scene):
    b = CONNECT_BRIDGE()
    lights = b.get_light_objects('list')

    # set RGB   
    for i in range(len(rgb_scene)):
        if rgb_scene[i] is not None:
            # get the rgb values only (source: rgb(xxx, xxx, xxx))
            rgb_color = re.findall(r'\d+', rgb_scene[i])     
            # convert rgb to xy    
            xy = RGBtoXY(int(rgb_color[0]), int(rgb_color[1]), int(rgb_color[2]))
            lights[i].xy = xy


def LED_SET_SCENE(scene, brightness_global = 100):
    b = CONNECT_BRIDGE()
    lights = b.get_light_objects('list')
    for light in lights:
        light.on = False

    from LED_database import GET_SCENE

    # get scene settings
    entries = GET_SCENE(scene)
    if entries[0] is not None:
        entries = entries[0]
        for entry in entries:
                # convert rgb to xy  
                xy = RGBtoXY(entry.color_red, entry.color_green, entry.color_blue)
                brightness = entry.brightness

                lights[entry.LED_id - 1].on = True
                lights[entry.LED_id - 1].xy = xy
             
                # set brightness
                brightness = int(brightness * (int(brightness_global) / 100))
                if brightness > 10:
                    lights[entry.LED_id - 1].brightness = brightness
                else:
                    lights[entry.LED_id - 1].on = False               


                



#b = Bridge('192.168.1.99')
#b.connect()

#print(b.get_api())

#lights = b.get_light_objects('id')

#print(lights)

#print(lights[2].brightness)

#lights[1].brightness = 254 #max

#xy = RGBtoXY(110,70,0)
#lights[1].xy = [xy[0], xy[1]]

#lights[1].on = True
#lights[1].on = False


