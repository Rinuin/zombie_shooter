import sys

from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import WindowProperties, Vec3, CollisionHandlerPusher, CollisionTraverser

from Scripts import MUSIC_START_1_ASSET
from Scripts.config import SCREEN_WIDTH, SCREEN_HEIGHT
from Scripts.player import Player
from Scripts.scene import Scene


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        properties = WindowProperties()
        properties.setSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.win.requestProperties(properties)
        self.disableMouse()

        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.pusher.setHorizontal(True)

        self.scene = Scene(self.render, self.loader, self, 5)
        self.player = Player("models/panda", {"walk": "models/panda-walk"}, 2, 15, "player",
                             self, Vec3(0, 0, 0), Vec3(180, 0, 0))
        self.camera_init()

        self.control_service()
        self.updateTask = taskMgr.add(self.update, "update")
        self.mouse_check_value = 0.7
        self.pusher.add_in_pattern("%fn-into-%in")


        # self.music = self.loader.load_music(MUSIC_START_1_ASSET)
        # self.music.setLoop(True)
        # self.music.play()

    def control_service(self):
        self.keyMap = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "shoot": False,
            "quit": False
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
        self.accept("escape", self.update_key_map, ["quit", True])

    def update_key_map(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def update(self, task):
        # Get the amount of time since the last update
        dt = globalClock.getDt()

        # If any movement keys are pressed, use the above time
        # to calculate how far to move the character, and apply that.
        if self.keyMap["up"]:
            self.player.move(Vec3(0, -  dt, 0))
        if self.keyMap["down"]:
            self.player.move(Vec3(0, dt, 0))
        if self.keyMap["left"]:
            self.player.move(Vec3(dt, 0, 0))
        if self.keyMap["right"]:
            self.player.move(Vec3(- dt, 0, 0))
        if self.keyMap["quit"]:
            self.exit_game()
        if self.mouseWatcherNode.hasMouse():
            if self.mouseWatcherNode.getMouseX() < -self.mouse_check_value:
                self.player.rotate(Vec3(100.0 * dt, 0, 0))
            elif self.mouseWatcherNode.getMouseX() > self.mouse_check_value:
                self.player.rotate(Vec3(-100.0 * dt, 0, 0))
        if self.keyMap["shoot"]:
            self.player.shoot()

        if not (self.keyMap["up"] or self.keyMap["down"] or self.keyMap["left"] or self.keyMap["right"]):
            self.player.stop()

        self.scene.update(dt)

        return task.cont

    def camera_init(self):
        x, y, z = self.player.get_position()
        self.camera.setPos(Vec3(x, y + 10, z + 17))
        self.camera.setHpr(180, -15, 0)
        self.camera.reparentTo(self.player.actor)

    def exit_game(self):
        # De-initialization code goes here!
        sys.exit()




