from Platform import *
import unittest


class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_default_size(self):
        self.assertEqual(str(self.player.image), str(pygame.Surface([40, 50])))

    def test_default_speed(self):
        self.assertEqual([self.player.change_x, self.player.change_y], [0, 0])

    def test_default_level(self):
        self.assertEqual(self.player.level, None)

    def test_default_direction(self):
        self.assertEqual(self.player.direction, "R")

    def test_sprite(self):
        sprite_sheet = SpriteSheet("boy.png")
        self.assertEqual(str(self.player.walking_frames_r), str([sprite_sheet.get_image(20, 3, 40, 50),
                                                                 sprite_sheet.get_image(80, 3, 40, 50),
                                                                 sprite_sheet.get_image(140, 3, 40, 50),
                                                                 sprite_sheet.get_image(200, 3, 40, 50)]))
        self.assertEqual(str(self.player.walking_frames_l),
                         str([pygame.transform.flip(sprite_sheet.get_image(20, 3, 40, 50), True, False),
                              pygame.transform.flip(sprite_sheet.get_image(80, 3, 40, 50), True, False),
                              pygame.transform.flip(sprite_sheet.get_image(140, 3, 40, 50), True, False),
                              pygame.transform.flip(sprite_sheet.get_image(200, 3, 40, 50), True, False)]))

    '''
    def test_update(self):
        x = self.player.rect.x
        y = self.player.rect.y
        x_change = self.player.change_x
        y_change = self.player.change_y
        self.player.update()
        self.assertEqual(self.player.rect.x, x + x_change)
        self.assertEqual(self.player.rect.y, y + y_change)

    '''

    def test_grav(self):
        self.player.calc_grav()
        self.assertEqual(self.player.change_y, 1)

    def test_jump(self):
        self.player.level = Level_00(self.player)
        self.player.jump()
        self.assertEqual(self.player.change_y, -10)
        self.assertEqual(self.player.rect.y, 0)

    def test_go_left(self):
        self.player.go_left()
        self.assertEqual(self.player.change_x, -6)
        self.assertEqual(self.player.direction, "L")

    def test_go_right(self):
        self.player.go_right()
        self.assertEqual(self.player.change_x, 6)
        self.assertEqual(self.player.direction, "R")

    def test_stop(self):
        self.player.stop()
        self.assertEqual(self.player.change_x, 0)


class BulletTestCase(unittest.TestCase):

    def setUp(self):
        self.bullet = Bullet(pos=0)

    def test_inits(self):
        self.assertEqual(self.bullet.pos, pg.math.Vector2(0))
        self.assertEqual(self.bullet.vel, pg.math.Vector2(450, 0))
        self.assertEqual(self.bullet.damage, 10)


class EnemyTestCase(unittest.TestCase):

    def setUp(self):
        self.enemy = Enemy()

    def test_inits(self):
        self.assertEqual(str(self.enemy.image), str(pygame.Surface([50, 50])))
        self.assertEqual(self.enemy.change_y, 0)
        self.assertEqual(self.enemy.change_x, 0)
        self.assertEqual(self.enemy.counter, 0)

    def test_setPosition(self):
        self.enemy.setPosition(0, 100)
        self.assertEqual(self.enemy.rect.left, 0)
        self.assertEqual(self.enemy.rect.top, 100)

    def test_enemy_sprite(self):

        self.assertEqual(str(self.enemy.walking_frames_r), str([sprite_sheet.get_image(0, 0, 45, 60),
                                                                sprite_sheet.get_image(45, 0, 45, 60),
                                                                sprite_sheet.get_image(90, 0, 45, 60),
                                                                sprite_sheet.get_image(135, 0, 45, 60),
                                                                sprite_sheet.get_image(180, 0, 45, 60),
                                                                sprite_sheet.get_image(225, 0, 45, 60),
                                                                sprite_sheet.get_image(265, 0, 45, 60)]))
        self.assertEqual(str(self.enemy.walking_frames_l),
                         str([pygame.transform.flip(sprite_sheet.get_image(0, 0, 45, 60), True, False),
                              pygame.transform.flip(sprite_sheet.get_image(45, 0, 45, 60), True, False),
                              pygame.transform.flip(sprite_sheet.get_image(90, 0, 45, 60), True, False),
                              pygame.transform.flip(sprite_sheet.get_image(135, 0, 45, 60), True, False),
                              pygame.transform.flip(sprite_sheet.get_image(180, 0, 45, 60), True, False),
                              pygame.transform.flip(sprite_sheet.get_image(225, 0, 45, 60), True, False),
                              pygame.transform.flip(sprite_sheet.get_image(265, 0, 45, 60), True, False)]))


class PlatformTestCase(unittest.TestCase):

    def setUp(self, width=0, height=0):
        self.platform = Platform(width, height)
        self.platform.width = width
        self.platform.height = height

    def test_inits(self):
        self.assertEqual(str(self.platform.image), str(pygame.Surface([self.platform.width, self.platform.height])))
        self.assertEqual(self.platform.rect, self.platform.image.get_rect())


class LevelTestCase(unittest.TestCase):

    def setUp(self):
        player = Player()
        self.level = Level(player)

    def test_inits(self):
        self.assertEqual(str(self.level.platform_list), '<Group(0 sprites)>')
        self.assertEqual(str(self.level.enemy_list), '<Group(0 sprites)>')
        self.assertEqual(self.level.world_shift, 0)

    def test_shift_world(self):
        self.level.shift_world(5)
        self.assertEqual(self.level.world_shift, 5)


class Level00TestCase(unittest.TestCase):

    def setUp(self):
        self.player = Player()
        self.level = Level_00(self.player)

    def test_inits(self):
        self.assertEqual(self.level.level_limit, -1400)
        self.assertEqual(self.level.level_limit_back, 200)
        self.assertEqual(str(self.level.enemy_list), '<Group(1 sprites)>')

    def test_platforms(self):
        self.assertEqual(str(self.level.platform_list), '<Group(16 sprites)>')


class Level01TestCase(unittest.TestCase):

    def setUp(self):
        self.player = Player()
        self.level = Level_01(self.player)

    def test_inits(self):
        self.assertEqual(self.level.level_limit, -1300)
        self.assertEqual(self.level.level_limit_back, 200)
        self.assertEqual(str(self.level.enemy_list), '<Group(2 sprites)>')

    def test_platforms(self):
        self.assertEqual(str(self.level.platform_list), '<Group(16 sprites)>')


class Level02TestCase(unittest.TestCase):

    def setUp(self):
        self.player = Player()
        self.level = Level_02(self.player)

    def test_inits(self):
        self.assertEqual(self.level.level_limit, -1500)
        self.assertEqual(self.level.level_limit_back, 200)
        self.assertEqual(str(self.level.enemy_list), '<Group(4 sprites)>')

    def test_platforms(self):
        self.assertEqual(str(self.level.platform_list), '<Group(13 sprites)>')


class Level03TestCase(unittest.TestCase):

    def setUp(self):
        self.player = Player()
        self.level = Level_03(self.player)

    def test_inits(self):
        self.assertEqual(self.level.level_limit, -1400)
        self.assertEqual(self.level.level_limit_back, 200)

    def test_platforms(self):
        self.assertEqual(str(self.level.platform_list), '<Group(18 sprites)>')


class Level04TestCase(unittest.TestCase):

    def setUp(self):
        self.player = Player()
        self.level = Level_04(self.player)

    def test_inits(self):
        self.assertEqual(self.level.level_limit, -1400)
        self.assertEqual(self.level.level_limit_back, 200)
        self.assertEqual(str(self.level.enemy_list), '<Group(1 sprites)>')

    def test_platforms(self):
        self.assertEqual(str(self.level.platform_list), '<Group(19 sprites)>')


if __name__ == '__main__':
    unittest.main()