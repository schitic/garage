from GarageDeamon.Common import ActorBase
import RPi.GPIO as GPIO
import time


class LocalDoor(ActorBase):

    def __init__(self, outputPin=24, local=True):
        self.commandPin = outputPin
        if local:
            self.pinDoorBlock = 10
            self._setup()
        super(LocalDoor, self).__init__()

    def run(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.log.write("Sent command", 'ACTION',
                       component_id=self.actor_name)
        GPIO.setup(self.commandPin, GPIO.OUT)
        GPIO.output(self.commandPin, False)
        time.sleep(2)
        GPIO.cleanup(self.commandPin)

    def obstacoleDetected(self):
        try:
            if GPIO.input(self.pinDoorClosed):
                self.obsacole = True
                self.log.write("Obstacle detected", 'STAUTS',
                               component_id="LocalDoor")
            else:
                self.obsacole = False
                self.log.write("Obstacle NOT detected", 'STAUTS',
                               component_id="LocalDoor")
        except Exception as _:
            pass

    def _setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.pinDoorBlock, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.pinDoorBlock, GPIO.RISING)

        # Callback functions
        GPIO.add_event_callback(self.pinDoorBlock, self.obstacoleDetected)
        print("AICI")
