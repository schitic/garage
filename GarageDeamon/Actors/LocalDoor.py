from GarageDeamon.Common import ActorBase
import RPi.GPIO as GPIO
import time


class LocalDoor(ActorBase):

    def __init__(self, outputPin=13):
        self.commandPin = outputPin
        self._setup()
        super(LocalDoor, self).__init__()

    def _setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.commandPin, GPIO.OUT)

    def run(self):
        GPIO.output(self.commandPin, False)
        time.sleep(2)
        GPIO.output(self.commandPin, True

