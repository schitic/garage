from GarageDeamon.Common import ActorBase
import RPi.GPIO as GPIO
import time


class LocalDoor(ActorBase):

    def __init__(self, outputPin=24):
        self.commandPin = outputPin
        super(LocalDoor, self).__init__()

    def run(self):
        print(self.commandPin)
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.commandPin, GPIO.OUT)
        GPIO.output(self.commandPin, False)
        time.sleep(2)
        GPIO.cleanup(self.commandPin)
