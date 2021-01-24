from direct.actor.Actor import Actor
from panda3d.core import Vec3


class Player:
    def __init__(self, parent):
        self.player_init(parent)

    def player_init(self, parent):
        self.actor = Actor("models/panda",
                           {"walk": "models/panda-walk"})
        self.actor.reparentTo(parent)
        #

    def get_position(self):
        return self.actor.getPos()

    def move(self, movement_vector):
        anim_controler = self.actor.getAnimControl("walk")
        if not anim_controler.isPlaying():
            self.actor.play("walk")
        self.actor.setPos(self.actor, movement_vector)

    def rotate(self, angle):
        self.actor.setHpr(self.actor, angle)

    def stop(self):
        anim_controler = self.actor.getAnimControl("walk")
        anim_controler.stop()
