from direct.actor.Actor import Actor
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import CollisionRay, CollisionHandlerQueue, CollisionNode



class Player:
    def __init__(self, parent):
        self.player_init(parent)

        self.ray = CollisionRay(0, 0, 0, 0, 1, 0)

        rayNode = CollisionNode("playerRay")
        rayNode.addSolid(self.ray)

        self.rayNodePath = parent.attachNewNode(rayNode)
        self.rayQueue = CollisionHandlerQueue()

        self.actor.cTrav.addCollider(self.rayNodePath, self.rayQueue)

        self.damagePerSecond = -5.0

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
            hitPos = rayHit.getSurfacePoint(self.actor.render)

            hitNodePath = rayHit.getIntoNodePath()
            print(hitNodePath)
            if hitNodePath.hasPythonTag("owner"):
                hitObject = hitNodePath.getPythonTag("owner")
                hitObject.alterHealth(self.damagePerSecond * dt)
