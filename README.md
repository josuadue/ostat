# ostat
This project allows you to display importent information about your system on a 128x32px oled display. To control the oled display an Adafruit library is used. 

## Instalation
An appropriate oled display has to be connected via I²C. After that just download the files and add the following line to your **/etc/rc.local** file.

For one static Page (containing: Wifi-Signal, IP, CPU-%, CPU-Temp, RAM-% and RAM-space).
```
python3 [path_to_stats.py]/stats.py static
```
![alt text](https://github.com/josuadue/ostat/blob/main/example/static.png "Static Display")


For four alternating Pages.
```
python3 [path_to_stats.py]/stats.py scrol
```
![alt text](https://github.com/josuadue/ostat/blob/main/example/scrol0.png "Static Display")
![alt text](https://github.com/josuadue/ostat/blob/main/example/scrol1.png "Static Display")
![alt text](https://github.com/josuadue/ostat/blob/main/example/scrol2.png "Static Display")
![alt text](https://github.com/josuadue/ostat/blob/main/example/scrol3.png "Static Display")
