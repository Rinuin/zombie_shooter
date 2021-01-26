from panda3d.core import Vec3

from Scripts.game_object import GameObject


class Player(GameObject):
    def __init__(self, modelName, model_anims, max_health, speed, collider_name,  base, pos, hpr=Vec3(0, 0, 0),
                 scale=1.0):
        GameObject.__init__(self, modelName, model_anims, max_health, speed, collider_name,  base, pos, hpr,
                            scale)
        self.player_init()

    def player_init(self):
        self.base.pusher.addCollider(self.collider, self.actor)
        self.base.cTrav.addCollider(self.collider, self.base.pusher)
        self.collider.setPythonTag("player", self)

    def move(self, movement_vector):
        anim_controller = self.actor.getAnimControl("walk")
        if not anim_controller.isPlaying():
            self.actor.play("walk")
        self.actor.setPos(self.actor, movement_vector * self.speed)

    def stop(self):
        anim_controller = self.actor.getAnimControl("walk")
        anim_controller.stop()

