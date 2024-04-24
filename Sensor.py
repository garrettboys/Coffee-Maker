import RPi.GPIO as GPIO
import time   

# Front sensor
trigger_pin_1 = 18
echo_pin_2 = 12

# Constant
SPEED_OF_SOUND_CM_S = 34416 # speed of sound constant at 71f, just took the avg for best precision

# Inits GPIO unit for sensor
def initGPIO(trg, echo):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(echo, GPIO.IN)
    GPIO.setup(trg, GPIO.OUT)

def getDistance(trg, echo): # trigger/echo pins of sensor
    # Sends a pulse to trigger the sensor
    GPIO.output(trg, True)
    time.sleep(0.00001)
    GPIO.output(trg, False)

    # Waits for the echo response
    pulse_start = time.time()
    pulse_end = time.time()

    while GPIO.input(echo) == 0:
        pulse_start = time.time()

    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    # Calculates pulse duration to get distance
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * SPEED_OF_SOUND_CM_S
    distance = round(distance, 2)

    return distance

# For front sensor
initGPIO(trigger_pin_1, echo_pin_2)

try:
    while True:
        distance = getDistance(trigger_pin_1, echo_pin_2)
        print("Distance:", distance, "cm")
except KeyboardInterrupt:
    GPIO.cleanup()
