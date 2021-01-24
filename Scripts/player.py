from direct.actor.Actor import Actor
from panda3d.core import Vec3


class Player:
    def __init__(self, parent):
        self.player_init(parent)

    def player_init(self, parent):
        self.actor = Actor("models/panda",
                           {"walk": "models/panda-walk"})
        self.actor.reparentTo(parent)
        self.actor.setPos(0, 5, 5)
        self.actor.setHpr(180, 0, 0)
        self.actor.loop("walk")

    def get_position(self):
        return self.actor.getPos()

    def move(self, movement_vector):
        self.actor.setPos(self.actor.getPos() + movement_vector)
