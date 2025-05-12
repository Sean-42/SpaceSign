from machine import Pin, I2C, ADC
import urequests
import ujson  # Use json if ujson isn't available
import network
import time
import tm1637
from ssd1306 import SSD1306_I2C
from xglcd_font import XglcdFont
import ssd1309
import framebuf,sys
import ssdTest

pix_res_x  = 128 # SSD1306 horizontal resolution
pix_res_y = 64   # SSD1306 vertical resolution
i2c_dev = I2C(1,scl=Pin(3),sda=Pin(2),freq=200000)  # start I2C on I2C1 (GPIO 26/27)

#oled = SSD1306_I2C(pix_res_x, pix_res_y, i2c_dev) # oled controller
#ssid = 'Panic! At the Cisco'
#password = 'TheC00leyF00lies'
#mydisplay = tm1637.TM1637(clk=Pin(27), dio=Pin(26))
ssid = 'DESKTOP-44QTM0N6657'
password = 'Bruteforce1337!'
wlan = network.WLAN(network.STA_IF)
wlan.disconnect()
wlan.active(True)
wlan.connect(ssid, password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
ip = wlan.ifconfig()[0]
print(f'Connected on {ip}')
i2c = I2C(1, freq=400000, scl=Pin(3), sda=Pin(2))

display = ssd1309.Display(i2c=i2c, rst=Pin(4))
#display = ssdTest.SSD1306_I2C(128, 64, i2c)
print("Loading fonts.  Please wait.")
wendy = XglcdFont('fonts/Wendy7x8.c', 7, 8)
nasa = XglcdFont('nasa.c',8,9)
api_url = "http://api.open-notify.org/astros.json"
#print(response.text)
response = None
while True:
    try:
        response = urequests.get(api_url)

        if response.status_code == 200:
            # Parse the JSON data
            data = ujson.loads(response.text)

            # Extract specific fields
            number_of_people = data.get("number", 0)
            people = data.get("people", [])
            message = data.get("message", "No message")
            AstroSave = []
            AstroCraft = []
            # Print the total number of astronauts
            print(f"Message: {message}")
            print(f"Number of people in space: {number_of_people}")
            fancyNum = f"{number_of_people:02d}"
            #mydisplay.show(fancyNum)
            #oled.text(fancyNum, 0, 10,1)
            #oled.show()
            # Print each astronaut's details
            print("\nList of astronauts:")
            
            i = 0
            for person in people:
                
                name = person.get("name", "Unknown")
                AstroSave.append(name)
                craft = person.get("craft", "Unknown")
                AstroCraft.append(craft)
                #print(f"{name} is on {craft}")
                #print(AstroSave[i])
        
                i = i + 1
            b = 0
            c = 0
            for b in range(600):
                for c in range(len(AstroSave)):
                    display.draw_text(6,8,AstroSave[c] +" - "+ AstroCraft[c],wendy)
                    display.present()
                    time.sleep(1)
                    display.scroll(0,8)
                    
                
            
            display.draw_text(6,8,"Checking Again in one minute",wendy)
            display.present()
            time.sleep(60)
            display.clear()
            display.present()
            
            
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
    except KeyboardInterrupt:
        print("BYE")
        wlan.disconnect()
    finally:
        # Safely close the response if it's defined and not None
        if response and hasattr(response, 'close'):
            response.close()