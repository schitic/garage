from GarageDeamon.Common import SensorBase
import RPi.GPIO as GPIO
import threading
import time

class CarSensorLeft(SensorBase):

    def __init__(self, ledRed=13, ledGreed=6, busI2C=3, position="left"):
        self.pinLedRed = ledRed
        self.pinLedGreed = ledGreed
        self.position = position
        self.busI2C = busI2C
        self._is_running = False
        super(CarSensorLeft, self).__init__()

    def html_hook(self):
        status = 'led-red'
        if self.get_db_state() == 'Present':
            status = 'led-green'
        html = '<div class="led-box"><div class="%s">' \
               '</div><p><strong>%s</strong> - %s</p>' \
               '</div>' % (status, self.sensor_name, self.get_db_state())
        return html

    def _listener(self):
        while self._is_running:
            print "Worker"
            time.sleep(1)

    def run(self):
        self._setup()
        self._is_running = True
        t = threading.Thread(target=self._listener)
        t.start()

    def close(self):
        print("IJN" + self._is_running)
        self._is_running = False

    def _current_state(self):
        return "Present"

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
