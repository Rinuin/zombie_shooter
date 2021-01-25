from panda3d.core import Vec3
from direct.actor.Actor import Actor

class Bullet(object):

    def __init__(self, actor, node, pos, hpr):
        self.actor = actor
        self.node = node
        self.node.setPosHpr(pos, hpr)
        self.speed = -20.0
        self.life = 5.0
        self.alive = True

    def update(self, dt):
        if not self.alive:
            return

        self.life -= dt

        if self.life > 0:
            # You should use the "fluid" versions of these functions
            # if you intend them to work with the collision system.
            self.actor.setPos(self.actor, Vec3(0, -self.speed * dt, 0))
            # self.node.setFluidY(self.node, self.speed * dt)
        else:
            self.node.removeNode()
            self.alive = False


