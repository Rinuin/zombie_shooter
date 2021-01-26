from panda3d.core import Vec3, BitMask32
from direct.actor.Actor import Actor
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import CollisionRay, CollisionHandlerQueue, CollisionNode

from direct.actor.Actor import Actor, CollisionNode
from panda3d.core import Vec3, CollisionSphere, CollisionCapsule, CollisionHandlerPusher

from Scripts import BAMBOO_LASER
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


        self.base.camLens.setFov(150) #----------------------------------------------
        # self.base.camLens.setFov(5)

        self.mask = BitMask32()
        self.mask.setBit(1)
        self.collider.node().setIntoCollideMask(self.mask)
        self.collider.node().setFromCollideMask(self.mask)

        self.mask.setBit(2)


        self.ray = CollisionRay(0, 0, 0, 0, -1, 0)

        rayNode = CollisionNode("playerRay")
        rayNode.addSolid(self.ray)

        mask = BitMask32()

        self.rayNodePath = self.actor.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()

        self.base.cTrav.addCollider(self.rayNodePath, self.rayQueue)

        self.damagePerSecond = -5.0
        self.beamModel = self.base.loader.loadModel("models/box")
        self.beamModel.reparentTo(self.actor)
        self.beamModel.setZ(2)

        self.beamModel.setLightOff()
        self.beamModel.hide()

    def move(self, movement_vector):
        anim_controller = self.actor.getAnimControl("walk")
        if not anim_controller.isPlaying():
            self.actor.play("walk")
        self.actor.setPos(self.actor, movement_vector * self.speed)

    def stop(self):
        anim_controller = self.actor.getAnimControl("walk")
        anim_controller.stop()


    def shoot(self):
        dt = globalClock.getDt()
        # print(self.rayQueue.getNumEntries())
        # print(self.rayQueue)
        if self.rayQueue.getNumEntries() > 0:
            self.rayQueue.sortEntries()
            rayHit = self.rayQueue.getEntry(1)
            hitPos = rayHit.getSurfacePoint(self.base.render)
            # print(hitPos, "hitpos")
            # print(rayHit, "rayhit")
            beamLength = (hitPos - self.actor.getPos())
            # print("length: ", beamLength)

            hitNodePath = rayHit.getIntoNodePath()
            # print(hitNodePath)
            # print(hitNodePath.getPythonTag)
            # print(hitPos)
            print(hitNodePath.getPythonTag)
            if hitNodePath.getPythonTag == "enemy":
                print("here")
                hitObject = hitNodePath.getPythonTag("enemy")
                hitObject.alterHealth(self.damagePerSecond * dt)
                # Find out how long the beam is, and scale the
                # beam-model accordingly.
                beamLength = (hitPos - self.actor.getPos()).length()
                self.beamModel.setSy(beamLength)

                self.beamModel.show()
        else:
            # If we're not shooting, don't show the beam-model.
            self.beamModel.hide()
