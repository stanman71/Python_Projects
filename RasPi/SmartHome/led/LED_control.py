from phue import Bridge
from RBGtoXY import RGBtoXY

"""

b = Bridge('192.168.1.99')

b.connect()
#print(b.get_api())

lights = b.get_light_objects('id')

print(lights)

lights[1].name
lights[1].brightness = 254 #max

#xy = RGBtoXY(0,0,0)
#lights[1].xy = [xy[0], xy[1]]

lights[1].on = True
#lights[1].on = False

"""

def CONNECT_BRIDGE():
   
    from LED_database import GET_BRIDGE_IP
    b = Bridge(GET_BRIDGE_IP())
    b.connect() 

    return b       


def LED_SET_BRIGHTNESS_GLOBAL(brightness):

    b = CONNECT_BRIDGE()

    lights = b.get_light_objects('list')

    for light in lights:
        if brightness > 10:
                light.on = True
                light.brightness = brightness
        else:
                light.on = False   


