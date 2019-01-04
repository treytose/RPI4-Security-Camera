import RPi.GPIO as GPIO
import time
import camera

alarmPin = 11
trigPin = 16
echoPin = 18
alarmSafePin = 13
MAX_DISTANCE = 420          #define the maximum measured distance
timeOut = MAX_DISTANCE*60   #calculate timeout according to the maximum measured distance

# Security #
cooldownTime = 60 #time for security to reactive after being triggered (in seconds)

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(alarmPin, GPIO.OUT)
    GPIO.setup(trigPin, GPIO.OUT)
    GPIO.setup(echoPin, GPIO.IN)
    GPIO.setup(alarmSafePin, GPIO.OUT)

def resetSecurity():
    time.sleep(2.5)
    f = open('security.txt', 'w')
    f.write('False')
    f.close()
    print('Security Reset')

def alarm():
    f = open('security.txt', 'r')
    securityText = f.readline()
    f.close()

    if securityText == 'True':
        print('Security is Disabled')
        resetSecurity()
        return

    GPIO.output(alarmPin, GPIO.HIGH)
    camera.take_picture()

    delay = 0.25
    for i in range(1, 10):
        GPIO.output(alarmPin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(alarmPin, GPIO.LOW)
        time.sleep(delay)

    GPIO.output(alarmPin, GPIO.LOW)
    camera.send_picture()

    print('Security on cooldown for {} seconds...'.format(cooldownTime))
    GPIO.output(alarmSafePin, GPIO.HIGH)
    time.sleep(cooldownTime)
    GPIO.output(alarmSafePin, GPIO.LOW)
    print('Security is now armed.')


def clean():
    GPIO.cleanup()

######### Sonar Thing #######
def pulseIn(pin,level,timeOut): # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime

def getSonar():     #get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH)      #make trigPin send 10us high level
    time.sleep(0.00001)     #10us
    GPIO.output(trigPin,GPIO.LOW)
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut)   #read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0     # the sound speed is 340m/s, and calculate distance
    return distance

def loop():
    while(True):
        distance = getSonar()
        print ("The distance is : %.2f cm"%(distance))
        if(distance < 100 and distance > 10):
            alarm()
        time.sleep(0.25)

setup()
try:
    loop()
except KeyboardInterrupt:  #when 'Ctrl+C' is pressed, the program will exit
    clean()
