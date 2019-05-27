from GarageDeamon.Common import SensorBase
import RPi.GPIO as GPIO


class CarSensorLeft(SensorBase):

    def __init__(self, ledRed=13, ledGreed=6, position="left"):
        self.pinLedRed = ledRed
        self.pinLedGreed = ledGreed
        self.position = position
        self._setup()
        super(CarSensorLeft, self).__init__()

    def _current_state(self):
        return "Not present"

    def car_present(self, _):
        if self.current_state == "Present":
            return
        GPIO.output(self.pinLedGreed, True)
        GPIO.output(self.pinLedRed, False)

        self.log.write("Car %s is Present" % self.position, 'STAUTS',
                       component_id=self.sensor_name)
        self.set_state("Present")

    def car_absent(self, _):
        if self.current_state == "Not present":
            return
        GPIO.output(self.pinLedGreed, False)
        GPIO.output(self.pinLedRed, True)
        self.log.write("Car %s is Present" % self.position, 'STAUTS',
                       component_id=self.sensor_name)
        self.set_state("Not present")

    def _setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.pinLedRed, GPIO.OUT)
        GPIO.setup(self.pinLedGreed, GPIO.OUT)

        if self._current_state() == "Present":
            GPIO.output(self.pinLedGreed, True)
            GPIO.output(self.pinLedRed, False)
        else:
            GPIO.output(self.pinLedGreed, False)
            GPIO.output(self.pinLedRed, True)
