from direct.actor.Actor import Actor
from panda3d.core import Vec3, CollisionNode, CollisionCapsule


class GameObject:
    def __init__(self, modelName, model_anims, max_health, speed, collider_name, render, base, pos, hpr=Vec3(0, 0, 0),
                 scale=1.0):
        self.actor = Actor(modelName, model_anims)
        self.actor.reparentTo(render)
        self.actor.setPos(pos)
        self.actor.setHpr(hpr)
        self.actor.setScale(Vec3(scale, scale, scale))
        self.base = base
        self.max_health = max_health
        self.health = max_health

        self.speed = speed

        colliderNode = CollisionNode(collider_name)
        colliderNode.addSolid(CollisionCapsule(Vec3(0, 0, 2) * 1 / scale, Vec3(0, 0, 9) * 1 / scale, 3 * 1 / scale))
        # colliderNode.addSolid(CollisionSphere(0, 0, 0, 0.3))
        self.collider = self.actor.attachNewNode(colliderNode)
        self.collider.setPythonTag("owner", self)

    def get_position(self):
        return self.actor.getPos()

    def rotate(self, angle):
        self.actor.setHpr(self.actor, angle)

    def change_health(self, dHealth):
        self.health += dHealth

        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health < 0:
            self.health = 0

    def cleanup(self):
        # Remove various nodes, and clear the Python-tag--see below!
        if self.collider is not None and not self.collider.isEmpty():
            self.collider.clearPythonTag("owner")
            self.base.cTrav.removeCollider(self.collider)
            self.base.pusher.removeCollider(self.collider)

        if self.actor is not None:
            self.actor.cleanup()
            self.actor.removeNode()
            self.actor = None

        self.collider = None
