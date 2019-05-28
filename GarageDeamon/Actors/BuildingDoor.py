from GarageDeamon.Actors.LocalDoor import LocalDoor


class BuildingDoor(LocalDoor):

    def __init__(self, outputPin=23):
        super(BuildingDoor, self).__init__(outputPin=outputPin)
