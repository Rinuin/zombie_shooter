from direct.actor.Actor import Actor
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import CollisionRay, CollisionHandlerQueue, CollisionNode

from direct.actor.Actor import Actor, CollisionNode
from panda3d.core import Vec3, CollisionSphere, CollisionCapsule, CollisionHandlerPusher


class Player:
    def __init__(self, parent, pusher, cTrav, loader):
        self.actor = None
        self.collider = None
        self.player_init(parent, pusher, cTrav, loader)


    def player_init(self, parent, pusher, cTrav, loader):
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

        self.parent = parent
        self.ray = CollisionRay(0, 0, 0, 0, 1, 0)

        rayNode = CollisionNode("playerRay")
        rayNode.addSolid(self.ray)

        self.rayNodePath = parent.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()

        cTrav.addCollider(self.rayNodePath, self.rayQueue)

        self.damagePerSecond = -5.0
        self.beamModel = loader.loadModel("models/misc/iris")
        self.beamModel.reparentTo(self.actor)
        # self.beamModel.setZ(1.5)

        # This prevents lights from affecting this particular node
        self.beamModel.setLightOff()
        # We don't start out firing the laser, so
        # we have it initially hidden.
        self.beamModel.hide()

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

    # def get_hpr(self):
    #     return self.actor.getHpr()

    # # Every frame this task calls update on each bullet in the bullets list.
    # def updateBullets(self, task):
    #     dt = globalClock.getDt()
    #
    #     for bullet in self.bullets:
    #         bullet.update(dt)
    #
    #     return task.cont

    def shoot(self):
        dt = globalClock.getDt()
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(0)
            hitPos = rayHit.getSurfacePoint(self.parent)

            hitNodePath = rayHit.getIntoNodePath()
            print(hitNodePath)
            print(hitNodePath.getPythonTag)
            # print(hitPos)
            if hitNodePath == "owner":
                print("here")
                hitObject = hitNodePath.getPythonTag("owner")
                hitObject.alterHealth(self.damagePerSecond * dt)
                # Find out how long the beam is, and scale the
                # beam-model accordingly.
                beamLength = (hitPos - self.actor.getPos()).length()
                self.beamModel.setSy(beamLength)

                self.beamModel.show()
        else:
            # If we're not shooting, don't show the beam-model.
            self.beamModel.hide()
