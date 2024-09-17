from ursina import *


class GentrysHouse(Entity):
    def __init__(self):
        super().__init__(
            model='quad',
            position=(0, 0),
            scale=(15, 12),
            color=rgb(147, 132, 31)
        )
