import pygame
import random
import sys
import os

pygame.init()

WIDTH = 400
HEIGHT = 700
FPS = 60
OBSTACLE_SIZE = 50

ASSETS_PATH = "assets"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)


class AssetManager:

    def __init__(self):
        self.player_img = None
        self.obstacle_img = None
        self.background_img = None
        self.load_all_assets()

    def load_all_assets(self):

        player_path = os.path.join(ASSETS_PATH, "mobil player.png")
        if os.path.exists(player_path):
            self.player_img = pygame.image.load(player_path).convert_alpha()
            print("Player image loaded!")
        else:
            print("mobil player.png' not found - using blue square")


        obstacle_path = os.path.join(ASSETS_PATH, "mobil obstakle 1.png")
        if os.path.exists(obstacle_path):
            self.obstacle_img = pygame.image.load(obstacle_path).convert_alpha()
            print("Obstacle image loaded!")
        else:
            print("mobil obstakle 1.png' not found - using red square")


        bg_path = os.path.join(ASSETS_PATH, "background.jpg")
        if os.path.exists(bg_path):
            self.background_img = pygame.image.load(bg_path).convert()
            self.background_img = pygame.transform.scale(self.background_img, (WIDTH, HEIGHT))
            print("Background loaded!")
        else:
            print("background.jpg' not found - using grey background")

    def get_player_image(self):
        if self.player_img:
            return pygame.transform.scale(self.player_img, (50, 50))
        else:
            img = pygame.Surface((50, 50))
            img.fill(BLUE)
            return img

    def get_obstacle_image(self):
        if self.obstacle_img:
            return pygame.transform.scale(self.obstacle_img, (OBSTACLE_SIZE, OBSTACLE_SIZE))
        else:
            img = pygame.Surface((OBSTACLE_SIZE, OBSTACLE_SIZE))
            img.fill(RED)
            return img

    def get_background(self):
        return self.background_img


class Player(pygame.sprite.Sprite):
    def __init__(self, asset_manager):
        super().__init__()
        self.asset_manager = asset_manager
        self.image = self.asset_manager.get_player_image()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_y = 0
        self.speed_x = 0

    def update(self):
        self.speed_y = 0
        self.speed_x = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed_x = 5
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed_y = -5
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed_y = 5

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # untuk batas layar
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, asset_manager, x, y):
        super().__init__()
        self.asset_manager = asset_manager
        self.image = self.asset_manager.get_obstacle_image()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("NEED MORE SPEED")
    clock = pygame.time.Clock()


    asset_manager = AssetManager()

    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    player = Player(asset_manager)
    all_sprites.add(player)

    score = 0
    obstacle_timer = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


        obstacle_timer += 1
        if obstacle_timer > 60:
            obs_x = random.randint(0, WIDTH - OBSTACLE_SIZE)
            obstacle = Obstacle(asset_manager, obs_x, -OBSTACLE_SIZE)
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
            obstacle_timer = 0

        all_sprites.update()


        if pygame.sprite.spritecollide(player, obstacles, False):
            print(f"\nGAME OVER! Final Skor: {score}")
            running = False

        score += 1


        bg = asset_manager.get_background()
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill(GREY)

        all_sprites.draw(screen)


        score_text = font.render(f"Skor: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()