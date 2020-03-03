from gpiozero import LED
import time

led = LED(2)

while True:
    time.sleep(1)
    led.toggle()
    
