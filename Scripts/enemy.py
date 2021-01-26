from panda3d.core import Vec3

from Scripts.game_object import GameObject


class Enemy(GameObject):
    def __init__(self, modelName, model_anims, max_health, speed, collider_name, render, base, pos, hpr=Vec3(0, 0, 0),
                 scale=1.0):
        GameObject.__init__(self, modelName, model_anims, max_health, speed, collider_name, render, base, pos, hpr,
                            scale)
