from panda3d.core import Vec3
from direct.actor.Actor import Actor
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import CollisionRay, CollisionHandlerQueue, CollisionNode

from direct.actor.Actor import Actor, CollisionNode
from panda3d.core import Vec3, CollisionSphere, CollisionCapsule, CollisionHandlerPusher

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
