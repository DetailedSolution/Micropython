# DHT11 Temperature and Humidity Sensor with different units for temperature displayed on LCD displayer and LED indicator for humidity
# Sensor reads temperature and humidity, and by the use of a push button we can toggle temperature display between Celsius and Fahrenheit
from machine import Pin
import utime as time # imports time from utime (time related functions)
from dht import DHT11 # imports DHT11 method from dht library
from lcd1602 import LCD # imports LCD method from lcd1602 library

pushButton =17
dataPin = 16
RedLED = 13  
GreenLED = 14
BlueLED = 15
data = Pin(dataPin, Pin.OUT, Pin.PULL_DOWN) # Using pin method, defines dataPin as output with pull_down resistor enablled
Sensor = DHT11 (data) # Sensor object
time.sleep(1) # Fixing operating system error (OSError: [Errno 110] ETIMEDOUT) with Sensor object and measurment method

ToggleButton = Pin(pushButton,Pin.IN,Pin.PULL_UP) # defines pushButton as input object

Temp= [0,0]  # A two dimensional array for storing temprature in two different units
TempUnit=['C','F'] # A two dimensional array for storing units of temperature

lcd=LCD()  # LCD object

#output LED object:
RLED = Pin(RedLED, Pin.OUT) 
GLED = Pin(GreenLED, Pin.OUT)
BLED = Pin(BlueLED, Pin.OUT)
#initializing LEDs states:
RLEDState = False  
GLEDState = False
BLEDState = False
RLED.value (RLEDState)   
GLED.value (GLEDState)
BLED.value (BLEDState)

CurrentTime = time.ticks_ms() # Current time in miliseconds

InterruptCount = 0
Index=0 # Initial index of the Temp and TempUnit

# Interrupt Service Routine (ISR) or Interrupt Handler: here ISR toggles the Index while the CPU is interrupted by a push button:
def InterruptHandler(pin):  
    global CurrentTime, Index, InterruptCount
#Multiple callbacks are trigered just by one interrupt request. But we can compare new time with old time and shift Index based on it:
    if ((time.ticks_ms()-CurrentTime) > 300): 
        CurrentTime = time.ticks_ms()
        InterruptCount = InterruptCount + 1
        Index=not Index # Swithing Index between 0 and 1
 #       print (Index)

ToggleButton.irq(trigger=Pin.IRQ_RISING, handler=InterruptHandler) # Triggers interrupt request from ToggleButton and calls handler.
# Where interrupt is on rising edge (i.e. after releasing push button). It could be on falling edge either (when button is pressed and
# not released yet).

def HumidityColor(): # using RGB LED indicator for differing range of humidity
    if (Humidity<= 50 ):
        GLEDState = True
        RLEDState = False        
        BLEDState = False
    if (50<=Humidity<= 70 ):
        GLEDState = False
        RLEDState = False      
        BLEDState = True
    if (Humidity>= 70 ):
        GLEDState = False
        RLEDState = True      
        BLEDState = False 
    RLED.value (RLEDState)   
    GLED.value (GLEDState)
    BLED.value (BLEDState)

print('My Sensor Data')
while True: 
    Sensor.measure()
    Temperature = Sensor.temperature()
    Humidity = Sensor.humidity()
    Temp[0] = Temperature
    Temp[1] = round(Temperature*(9/5)+32)
    print("\r" ,'Temperature=', Temp[Index],chr(176)+TempUnit[Index],' Humidity=',Humidity,'%', ' InterruptCount= ', InterruptCount, end=' ')
    HumidityColor()
    lcd.clear() 
    lcd.write(0,0,'Temp= '+str(Temp[Index])+chr(176)+str(TempUnit[Index]))
    lcd.write(0,1,' Humidity='+str(Humidity)+'%')
    time.sleep(1)     
