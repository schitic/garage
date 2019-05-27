#!/usr/local/bin/python
from GarageDeamon.Loader import ActorLoader, SensorLoader
from GarageDeamon.Logger import LogCreator
import logging


class GarageDeamon:
    def __init__(self):
        # Start logging
        self.log = LogCreator()

        # Load the sensors
        self.sensors = SensorLoader.get_modules()
        for sensor in self.sensors.keys():
            self.log.write('Sensor: %s' % sensor, 'Loaded')

        # Load the actors
        self.actors = ActorLoader.get_modules()
        for actor in self.actors.keys():
            self.log.write('Sensor: %s' % actor, 'Loaded')


if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)-8s: %(message)s")
    logging.getLogger().setLevel(logging.INFO)
    GarageDeamon()
