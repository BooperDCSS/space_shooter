import pygame
from pathlib import Path
from random import randint

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
CODE_DIR = Path(__file__).parent.resolve()
ROOT_DIR = Path(CODE_DIR).parent.resolve()

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(ROOT_DIR.joinpath("images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.groups = groups

        self.direction = pygame.math.Vector2()
        self.speed = 300

        # laser and cooldown attributes
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 2000 # ms

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks() # returns value in ms
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()

        #movement
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a]) # resolves to 1 or -1
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w]) # resolves to 1 or -1
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        # zee missiles!
        if pygame.key.get_just_pressed()[pygame.K_SPACE] and self.can_shoot:
            print("FIRE ZEE MISSILES!")
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer() # every update, run the laser_timer method

class Stars(pygame.sprite.Sprite):
    def __init__(self, groups, surface):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))


def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True

    # creating a window; note that this expects a tuple, not just two ints
    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    pygame.display.set_caption("Shooting... in space!!")

    # creating groups and sprites
    all_sprites = pygame.sprite.Group()

    star_surface = pygame.image.load(ROOT_DIR.joinpath("images", "star.png")).convert_alpha()
    for i in range(20):
        Stars(all_sprites, star_surface)
        # this works because group.draw calls blit on the object's .image and .rect
        # we define the surface ONCE so that we use the same surface over and over
        # rather than putting the surface in the class and loading it 20 times

    player = Player(all_sprites)

    # old methods to be removed
    meteor_surf = pygame.image.load(ROOT_DIR.joinpath("images", "meteor.png")).convert_alpha()
    meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

    laser_surf = pygame.image.load(ROOT_DIR.joinpath("images", "laser.png")).convert_alpha()
    laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

    # events
    meteor_event = pygame.event.custom_type()
    pygame.time.set_timer(meteor_event, 500)

    ### BEGINNING OF GAME LOOP HERE ###
    while running:
        dt = clock.tick(60) / 1000

        # this is my event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == meteor_event:
                print("METEOR EVENT IS HAPPENING!!!")


        all_sprites.update(dt)
        display_surface.fill("darkgray")

        # this is how we draw the game; after everything happens, draw and update!
        # .flip() can be used to update just a part of the window
        all_sprites.draw(display_surface)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
