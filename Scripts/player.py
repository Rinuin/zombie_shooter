from direct.actor.Actor import Actor, CollisionNode
from panda3d.core import Vec3, CollisionSphere, CollisionCapsule, CollisionHandlerPusher


class Player:
    def __init__(self, parent, pusher, cTrav):
        self.actor = None
        self.collider = None
        self.player_init(parent, pusher, cTrav)

    def player_init(self, parent, pusher, cTrav):
        self.actor = Actor("models/panda",
                           {"walk": "models/panda-walk"})
        self.actor.reparentTo(parent)
        self.actor.setHpr(180, 0, 0)
        self.actor.setPos(0, 0, 0)
        colliderNode = CollisionNode("player")
        # Add a collision-sphere centred on (0, 0, 0), and with a radius of 0.3
        colliderNode.addSolid(CollisionCapsule(Vec3(0, 0, 2), Vec3(0, 0, 9), 3))

        self.collider = self.actor.attachNewNode(colliderNode)
        pusher.addCollider(self.collider, self.actor)
        # The traverser wants a collider, and a handler
        # that responds to that collider's collisions
        cTrav.addCollider(self.collider, pusher)

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
