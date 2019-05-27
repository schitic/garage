from GarageDeamon.Common import SensorBase
import RPi.GPIO as GPIO
from GarageDeamon.Logger import LogCreator


class DoorSensor(SensorBase):

    def __init__(self):
        super(DoorSensor, self).__init__()
        self.pinDoorClosed = 20
        self.pinDoorOpen = 21
        self.log = LogCreator()
        self._setup()

    def door_opened(self, _):
        if self.current_state == "Opened":
            return
        self.log.write("Door is Open", 'STAUTS', component_id=self.sensor_name)
        self.set_state("Opened")

    def door_closed(self, _):
        if self.current_state == "Closed":
            return
        self.log.write("Door is Closed", 'STAUTS', component_id=self.sensor_name)
        self.set_state("Closed")

    def _setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.pinDoorClosed, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.pinDoorOpen, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        GPIO.add_event_detect(self.pinDoorClosed, GPIO.RISING)
        GPIO.add_event_detect(self.pinDoorOpen, GPIO.RISING)

        # Callback functions
        GPIO.add_event_callback(self.pinDoorClosed, self.door_closed)
        GPIO.add_event_callback(self.pinDoorOpen, self.door_opened)

