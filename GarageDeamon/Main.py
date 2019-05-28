#!/usr/local/bin/python
from GarageDeamon.Loader import ActorLoader, SensorLoader
from GarageDeamon.Logger import LogCreator
import logging

import signal
import sys



class GarageDeamon:
    def __init__(self):
        # Start logging
        self.log = LogCreator()
        signal.signal(signal.SIGINT, self.sigint_handler)

        # Load the sensors
        self.sensors = SensorLoader.get_modules()
        for sensor in self.sensors.keys():
            self.log.write('Sensor: %s' % sensor, 'Loaded')
            self.sensors[sensor].run()

        # Load the actors
        self.actors = ActorLoader.get_modules()
        for actor in self.actors.keys():
            self.log.write('Actors: %s' % actor, 'Loaded')

    def sigint_handler(self, signal, frame):
        for sensor in self.sensors.keys():
            self.sensors[sensor].close()

    def run(self):
        try:
            while True:
                continue
        except KeyboardInterrupt:
            for sensor in self.sensors.keys():
                self.sensors[sensor].close()
                return


if __name__ == '__main__':
    logging.basicConfig(format="%(levelname)-8s: %(message)s")
    logging.getLogger().setLevel(logging.INFO)
    garage = GarageDeamon()
    garage.run()
