from panda3d.core import Vec3, Vec2

from Scripts.game_object import GameObject


class Enemy(GameObject):
    def __init__(self, modelName, model_anims, max_health, speed, collider_name, render, base, pos, hpr=Vec3(0, 0, 0),
                 scale=1.0):
        GameObject.__init__(self, modelName, model_anims, max_health, speed, collider_name, render, base, pos, hpr,
                            scale)
        self.actor.loop("walk")
        self.target = base.player
        self.yVector = Vec2(0, 1)

    def attack(self, dt):
        vectorToPlayer = self.target.get_position() - self.actor.getPos()

        vectorToPlayer2D = vectorToPlayer.getXy()
        distanceToPlayer = vectorToPlayer2D.length()

        vectorToPlayer2D.normalize()

        heading = self.yVector.signedAngleDeg(vectorToPlayer2D)

        vectorToPlayer.setZ(0)
        #vectorToPlayer.normalize()
        velocity = vectorToPlayer * self.speed * dt

        self.actor.setH(heading+180)

        self.actor.setPos(self.get_position() + velocity * dt)
