import pygame
from pathlib import Path
from random import randint, uniform

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
        self.cooldown_duration = 400 # ms

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
            Laser(laser_surface, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()

        self.laser_timer() # every update, run the laser_timer method

class Stars(pygame.sprite.Sprite):
    def __init__(self, groups, surface):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surface, pos, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(midbottom = pos)

    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(midbottom = (randint(0, WINDOW_WIDTH), -1))
        self.start_time = pygame.time.get_ticks() # this triggers on creation

        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(200, 400)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= 4000:
            self.kill()

def laser_collisions():
    for laser in laser_sprites:
        laser_hits = pygame.sprite.spritecollide(laser, meteor_sprites, True, pygame.sprite.collide_mask)
        if laser_hits:
            laser.kill()

def display_score(font):
    current_time = pygame.time.get_ticks() // 100
    text_surface = font.render(str(current_time), True, "#eeeeee")
    text_rect = text_surface.get_frect(midbottom = ((WINDOW_WIDTH / 2), (WINDOW_HEIGHT - 50)))
    display_surface.blit(text_surface, text_rect)
    padded_rect = text_rect.inflate(20, 15).move(0, -5)
    pygame.draw.rect(display_surface, "red", padded_rect, 5, 5)

### CREATING GAME WINDOW AND TITLE (notice set_mode takes a tuple) ###
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Shooting... in space!!")

### CREATING GROUPS AND SPRITES ###
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()

### IMPORT SURFACES OUTSIDE CLASSES WHEN USED IN LOOP (only loads once) ###
star_surface = pygame.image.load(ROOT_DIR.joinpath("images", "star.png")).convert_alpha()
laser_surface = pygame.image.load(ROOT_DIR.joinpath("images", "laser.png")).convert_alpha()
meteor_surface = pygame.image.load(ROOT_DIR.joinpath("images", "meteor.png")).convert_alpha()


### CUSTOM EVENTS DEFINITIONS ###
meteor_event = pygame.event.custom_type()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True

    ### TEXT SURFACES ###
    # inside main() because pygame.init() is required and I'm using main()
    font = pygame.font.Font(ROOT_DIR.joinpath("images", "Oxanium-Bold.ttf"), 40)

    for i in range(20):
        Stars(all_sprites, star_surface)
        # this works because group.draw calls blit on the object's .image and .rect
        # we define the surface ONCE so that we use the same surface over and over
        # rather than putting the surface in the class and loading it 20 times

    player = Player(all_sprites)

    ### INITIATING EVENTS ###
    pygame.time.set_timer(meteor_event, 500)

    ### BEGINNING OF GAME LOOP HERE ###
    while running:
        dt = clock.tick(60) / 1000

        # this is my event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == meteor_event:
                Meteor(meteor_surface, (all_sprites, meteor_sprites))

        # update the sprites according to their update methods
        # and check for collisions
        all_sprites.update(dt)
        laser_collisions()

        # check for game-ending collision
        if pygame.sprite.spritecollide(player, meteor_sprites, False, pygame.sprite.collide_mask):
            print("Game over, man")
            running = False

        # this is how we draw the game; after everything happens, draw and update!
        # .flip() can be used to update just a part of the window
        display_surface.fill("#3a2e3f")
        all_sprites.draw(display_surface)
        display_score(font)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
