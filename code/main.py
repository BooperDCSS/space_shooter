import pygame
from pathlib import Path
from random import randint

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
CODE_DIR = Path(__file__).parent.resolve()
ROOT_DIR = Path(CODE_DIR).parent.resolve()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    running = True

    display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # creating a window; note that this expects a tuple, not just two ints

    pygame.display.set_caption("Shooting... in space!!")

    ### PLAIN SURFACE, PROBABLY REMOVE ###
    surf = pygame.Surface((100,200))
    surf.fill("white")

    ### IMPORTS ###
    player_surf = pygame.image.load(ROOT_DIR.joinpath("images", "player.png")).convert_alpha()
    player_rect = player_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
    player_direction = pygame.math.Vector2(2, -1)
    player_speed = 100
    ## the vector defaults to 0,0 if you don't provide x,y arguments 
    
    star_surf = pygame.image.load(ROOT_DIR.joinpath("images", "star.png")).convert_alpha()
    star_pos = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for i in range(20)]

    meteor_surf = pygame.image.load(ROOT_DIR.joinpath("images", "meteor.png")).convert_alpha()
    meteor_rect = meteor_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

    laser_surf = pygame.image.load(ROOT_DIR.joinpath("images", "laser.png")).convert_alpha()
    laser_rect = laser_surf.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

    while running:
        # this is my event loop
        dt = clock.tick(30) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display_surface.fill("darkgray")
        for pos in star_pos:
            display_surface.blit(star_surf, pos)
        # blit stands for block image transfer

        display_surface.blit(laser_surf, laser_rect)
        display_surface.blit(meteor_surf, meteor_rect)

        if player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
            player_direction.x *= -1
        if player_rect.bottom > WINDOW_HEIGHT or player_rect.top < 0:
            player_direction.y *= -1
        # the bouncing effect relies on just the x or y value modifying
        # if you modify both, it just bounces back and forth along a single trajectory
        # but modifying just the x or y changes the direction of the vector entirely

        player_rect.center += player_direction * player_speed * dt
        display_surface.blit(player_surf, player_rect)
        
        pygame.display.update()
        # and this is how we draw the game; after everything happens, update!
        # .flip() can be used to update just a part of the window

    pygame.quit()

if __name__ == "__main__":
    main()
