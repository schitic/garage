from GarageDeamon.Sensors.CarPresanceLeft import CarSensorLeft
import RPi.GPIO as GPIO


class CarSensorRight(CarSensorLeft):

    def __init__(self, ledRed=5, ledGreed=22, busI2C=4, position="right"):
        super(CarSensorRight, self).__init__(ledRed=ledRed, ledGreed=ledGreed,
                                             busI2C=busI2C,
                                             position=position)

    def _current_state(self):
        return "Not present"
