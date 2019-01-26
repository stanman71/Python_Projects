from phue import Bridge
import math
import sys

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




""" #################### """
""" brightness functions """
""" #################### """

def LED_SET_BRIGHTNESS_GLOBAL(brightness):
    b = CONNECT_BRIDGE()
    lights = b.get_light_objects('list')

    for light in lights:
        if brightness > 10:
                light.on = True
                light.brightness = brightness
        else:
                light.on = False   



#b = Bridge('192.168.1.99')
#b.connect()

#print(b.get_api())

#lights = b.get_light_objects('id')

#print(lights)

#lights[1].name
#lights[1].brightness = 254 #max

#xy = RGBtoXY(110,70,0)
#lights[1].xy = [xy[0], xy[1]]

#lights[1].on = True
#lights[1].on = False


