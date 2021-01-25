from math import copysign

from panda3d.core import SamplerState, CardMaker, CollisionNode, Vec3, CollisionPlane, Point3, Plane


class Scene:
    def __init__(self, render, loader):
        self.size = 200
        self.scene_init(render, loader)

    def scene_init(self, render, loader):
        # self.scene = self.loader.loadModel("models/environment")
        # self.scene.reparentTo(self.render)

        # region texture
        floor_texture = loader.loadTexture("models/maps/envir-ground.jpg")
        floor_texture.setMinfilter(SamplerState.FT_linear_mipmap_linear)

        wall_texture = loader.loadTexture("models/maps/envir-reeds.png")
        # endregion

        # region floor
        floor_card_maker = CardMaker("floor")
        floor_card_maker.setUvRange((0, 0), (self.size / 10, self.size / 10))
        floor_gfx = render.attachNewNode(CardMaker.generate(floor_card_maker))
        floor_gfx.setP(-90)  # This rotates the card to face upwards
        floor_gfx.setPos(-self.size / 2, -self.size / 2, 0)
        floor_gfx.setScale(self.size)

        floor_gfx.setTexture(floor_texture)
        # endregion

        # region walls

        self.create_wall(render, wall_texture, -90, 0, 0)
        self.create_wall_collider(render, 0, 1, -180)

        self.create_wall(render, wall_texture, 0, 90, -90)
        self.create_wall_collider(render, 0, -1, 0)

        self.create_wall(render, wall_texture, 90, -90, -180)
        self.create_wall_collider(render, 1, 0, 90)

        self.create_wall(render, wall_texture, -90, -90, -270)
        self.create_wall_collider(render, -1, 0, -90)

        # endregion

    def create_wall(self, render, wall_texture, x_angle, y_angle, angle):
        wall_card_maker = CardMaker("wall")
        wall_card_maker.setUvRange((0, 0), (self.size / 50, self.size / 50))
        wall_gfx = render.attachNewNode(CardMaker.generate(wall_card_maker))
        wall_gfx.setPos(copysign(1, x_angle) * self.size / 2, copysign(1, y_angle) * self.size / 2, 0)
        wall_gfx.setScale(self.size)
        wall_gfx.setHpr(angle, 0, 0)

        wall_gfx.setTransparency(True)
        wall_gfx.setTexture(wall_texture)

    def create_wall_collider(self, render, x_angle, y_angle, angle):
        wallSolid = CollisionPlane(Plane(Vec3(0, 0, 1), Point3(0, 0, 0)))
        wallNode = CollisionNode("wall")
        wallNode.addSolid(wallSolid)
        wall = render.attachNewNode(wallNode)

        wall.setX(x_angle * self.size / 2)
        wall.setY(y_angle * self.size / 2)

        wall.setHpr(angle, -90, 0)
