from panda3d.core import Vec3, Vec2

from Scripts.game_object import GameObject


class Enemy(GameObject):
    def __init__(self, modelName, model_anims, max_health, speed, collider_name, base, scene, pos, hpr=Vec3(0, 0, 0),
                 scale=1.0):
        GameObject.__init__(self, modelName, model_anims, max_health, speed, collider_name, base, pos, hpr,
                            scale)
        self.actor.loop("walk")
        self.target = base.player
        self.yVector = Vec2(0, 1)
        self.scene = scene

        self.base.accept("enemy-into-player", self.collision)
        self.base.accept("player-into-enemy", self.collision)

    def attack(self, dt):
        vectorToPlayer = self.target.get_position() - self.actor.getPos()

        vectorToPlayer2D = vectorToPlayer.getXy()
        vectorToPlayer2D.normalize()

        heading = self.yVector.signedAngleDeg(vectorToPlayer2D)

        vectorToPlayer.setZ(0)
        velocity = vectorToPlayer * self.speed * dt

        self.actor.setH(heading + 180)
        self.actor.setPos(self.get_position() + velocity * dt)

    def collision(self, entry):
        collider = entry.getFromNodePath()
        if collider.hasPythonTag("player"):
            self.base.player.change_health(-1)
            self.cleanup()

    def cleanup(self):
        GameObject.cleanup(self)
        self.scene.enemies.remove(self)
