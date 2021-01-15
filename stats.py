# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import sys
import time
from os import path

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import numpy as np


# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=None)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height

image = Image.new('1', (width, height))

# Load default font.
font = ImageFont.load_default()

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

#Set wether to use one main Page or multiple Scrolling Pages
if len(sys.argv) > 1:
    if sys.argv[1] == "scrol":
        UseScrollingPages = True
    elif sys.argv[1] == "static":
        UseScrollingPages = False
    else:
        sys.exit(0)
else:
    sys.exit(0)
#Define scrolling Pages that are shown. You can remove some or add your own
Pages = ["NetworkPage", "ProcessorPage", "MemoryPage", "StoragePage"]

#Seconds per Page
PageDuration = 2

#Seconds between updates (calling Systemfunctions to get the shown stats)
UpdateIntervall = 0.75


ImagePath = path.abspath(path.dirname(__file__)) + "/img/"
#Loading of Pictogram images
iwifi0 = Image.open(ImagePath + "wlan0.bmp")
iwifi1 = Image.open(ImagePath + "wlan1.bmp")
iwifi2 = Image.open(ImagePath + "wlan2.bmp")
iwifi3 = Image.open(ImagePath + "wlan3.bmp")
iwifi4 = Image.open(ImagePath + "wlan4.bmp")
 
idot0 = Image.open(ImagePath + "dot0.bmp")
idot1 = Image.open(ImagePath + "dot1.bmp")

icpu = Image.open(ImagePath + "cpu.bmp")
iram = Image.open(ImagePath + "ram.bmp")
ihdd = Image.open(ImagePath + "hdd.bmp")

#The last time the stats were updated (in ns since epoch)
LastUpdate = 0

#The last time the next Page was shown
LastPageTurn = time.time()

#The index of the current Page
i_page = 0

#Displayed Page
page = Pages[i_page]

WifiLinkQuality = 0
IP = "000.000.000.000"
CPUPercent = "??.?%"
CPUTemperature = "??.?°C"
mem_percent = "??.?%"
mem_used = "???/???"
hdd_percent = "??.?%"
hdd_used = "???/???GB"

#CPU Time 
cpu_time0 = 0
cpu_idle0 = 0
cpu_time1 = 0
cpu_idle1 = 0

while True:
    if UseScrollingPages == False:
        draw.rectangle((0,0,width-1,height-1), outline=0, fill=0)
        
        if WifiLinkQuality < 1:
            image.paste(iwifi1,(0,0))
        elif WifiLinkQuality < 2:
            image.paste(iwifi2,(0,0))
        elif WifiLinkQuality < 3:
            image.paste(iwifi3,(0,0))
        else:
            image.paste(iwifi4,(0,0))

        image.paste(icpu,(1,18))
        draw.text((20,13),CPUPercent, font=font, fill=255)
        draw.text((20,23),CPUTemperature, font=font, fill=255)

        image.paste(iram,(58,18))        
        draw.text((80,13),mem_percent, font=font, fill = 255)
        draw.text((80,23),mem_used, font=font, fill = 255) 

        draw.text((21,0),"IP:" + IP ,font=font, fill = 255)
        #image.paste(Image.open("oled.bmp"),(0,0))
    else:
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width-1,height-1), outline=0, fill=0)

        #circle0.load() = [[255,255,255,255],[255,255,255,255],[255,255,255,255],[255,255,255,255]]
        for i,value in enumerate(Pages):
            if page == value:
                image.paste(idot1,(80+8*i,0))
            else:
                image.paste(idot0,(80+8*i,0))

        if  page == "NetworkPage":
            draw.text((0,0), "Network:",font=font, fill=255)

            if WifiLinkQuality < 1:
                image.paste(iwifi1,(0,13))
            elif WifiLinkQuality < 2:
                image.paste(iwifi2,(0,13))
            elif WifiLinkQuality < 3:
                image.paste(iwifi3,(0,13))
            else:
                image.paste(iwifi4,(0,13))
                
            draw.text((21,18),"IP:" + IP ,font=font, fill = 255)

        if page == "ProcessorPage":
            draw.text((0,0), "Processor:",font=font, fill=255)
            
            image.paste(icpu,(11,14))
            draw.text((34,13),CPUPercent, font=font, fill=255)
            draw.text((73,13),CPUTemperature, font=font, fill=255)

        if page == "MemoryPage":
            draw.text((0,0), "Memory:",font=font, fill=255)
            
            image.paste(iram,(11,14))        
            draw.text((34,13),mem_percent, font=font, fill = 255)
            draw.text((69,13),mem_used, font=font, fill = 255) 
            
        if page == "StoragePage":
            draw.text((0,0), "Disk:",font=font, fill=255)
            
            image.paste(ihdd,(11,14))        
            draw.text((34,13),hdd_percent, font=font, fill = 255)
            draw.text((69,13),hdd_used, font=font, fill = 255) 
        
        draw.rectangle((0,height-2,int(width*min((time.time() - LastPageTurn)/PageDuration,1)),height-1),outline = 255, fill=255)
        
        if time.time()-LastPageTurn > PageDuration:
            LastPageTurn = time.time()
            i_page = (i_page+1)%len(Pages)
            page=Pages[i_page]

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)

    if time.time() > LastUpdate + UpdateIntervall:
        if page == "NetworkPage" or UseScrollingPages == False:
            cmd = 'iwconfig wlan0 | grep "Link Quality"'
            WifiLinkQuality = int(subprocess.check_output(cmd, shell = True ).decode('utf-8').split("=")[1].split("/")[0].strip())/17.5
        
            cmd = "hostname -I | cut -d\' \' -f1"
            IP = str(subprocess.check_output(cmd, shell = True ).decode('utf-8')).replace("\n","")

        if page == "ProcessorPage" or UseScrollingPages == False:
            cmd = "cat /proc/stat | grep cpu | head -n 1"
            CPU_string = str(subprocess.check_output(cmd, shell = True ).decode('utf-8')).split()
            cpu_time0 = int(CPU_string[1])+int(CPU_string[2])+int(CPU_string[3])
            cpu_idle0 = int(CPU_string[4])
            CPUPercent = str(round((cpu_time0-cpu_time1)/(cpu_time0-cpu_time1 + cpu_idle0-cpu_idle1)*100,1)) + "%"
            cpu_time1 = cpu_time0
            cpu_idle1 = cpu_idle0
        
            cmd = "vcgencmd measure_temp"
            CPUTemperature = str(subprocess.check_output(cmd, shell = True).decode('utf-8')).split('=')[1].split("'")[0] + "°C"

        if page == "MemoryPage" or UseScrollingPages == False:
            cmd = "free -m | grep Mem:"
            MEM = str(subprocess.check_output(cmd, shell = True ).decode('utf-8')).split()
            mem_used = str(int(MEM[1]) - int(MEM[3])) + "/" + str(int(MEM[1]))
            if UseScrollingPages == True:
                mem_used += " MB"
            mem_percent = str(round((1-(int(MEM[3])/int(MEM[1])))*100)) + "%"

        if page == "StoragePage" or UseScrollingPages == False:
            cmd = 'df | grep "/dev/root"'
            hdd_string = str(subprocess.check_output(cmd, shell = True).decode('utf-8')).split()
            hdd_used = str(round(int(hdd_string[2])*1e-6,1)) + "/" + str(round(int(hdd_string[1])*1e-6,1)) + "GB"
            hdd_percent = str(round(int(hdd_string[2])/int(hdd_string[1])*100,1)) + "%" 
        
        LastUpdate = time.time() 

