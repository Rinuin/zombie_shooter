from math import pi, sin, cos

from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import WindowProperties, Vec3
from direct.task import Task

from Scripts.player import Player


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)
        self.disableMouse()

        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)

        self.player = Player(self.render)
        self.camera_control()

        self.control_service()
        self.updateTask = taskMgr.add(self.update, "update")

    def control_service(self):
        self.keyMap = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "shoot": False
        }
        self.accept("w", self.update_key_map, ["up", True])
        self.accept("w-up", self.update_key_map, ["up", False])
        self.accept("s", self.update_key_map, ["down", True])
        self.accept("s-up", self.update_key_map, ["down", False])
        self.accept("a", self.update_key_map, ["left", True])
        self.accept("a-up", self.update_key_map, ["left", False])
        self.accept("d", self.update_key_map, ["right", True])
        self.accept("d-up", self.update_key_map, ["right", False])
        self.accept("mouse1", self.update_key_map, ["shoot", True])
        self.accept("mouse1-up", self.update_key_map, ["shoot", False])

    def update_key_map(self, controlName, controlState):
        self.keyMap[controlName] = controlState
        print(controlName, "set to", controlState)

    def update(self, task):
        # Get the amount of time since the last update
        dt = globalClock.getDt()

        # If any movement keys are pressed, use the above time
        # to calculate how far to move the character, and apply that.
        if self.keyMap["up"]:
            self.player.move(Vec3(0, 5.0 * dt, 0))
        if self.keyMap["down"]:
            self.player.move(Vec3(0, -5.0 * dt, 0))
        if self.keyMap["left"]:
            self.player.move(Vec3(-5.0 * dt, 0, 0))
        if self.keyMap["right"]:
            self.player.move(Vec3(5.0 * dt, 0, 0))
        if self.keyMap["shoot"]:
            print("Zap!")

        return task.cont


