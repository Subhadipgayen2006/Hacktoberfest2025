import pygame, random, sys
pygame.init()

# --- Screen setup ---
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 Galactic Defender")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# --- Classes ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT - 60))
        self.speed = 7

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(20, WIDTH - 20), -40))
        self.speed = random.randint(2, 6)

    def update(self, keys):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((6, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10

    def update(self, keys):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# --- Groups ---
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player()
all_sprites.add(player)
score = 0
spawn_timer = 0
game_over = False
font = pygame.font.SysFont("Arial", 28)

# --- Main Loop ---
while True:
    keys = pygame.key.get_pressed()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over and e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            player.shoot()
        if game_over and e.type == pygame.KEYDOWN and e.key == pygame.K_r:
            enemies.empty(); bullets.empty(); all_sprites.empty()
            player = Player(); all_sprites.add(player)
            score = 0; game_over = False

    if not game_over:
        spawn_timer += 1
        if spawn_timer > 25:
            spawn_timer = 0
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        all_sprites.update(keys)
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        score += len(hits) * 10
        if pygame.sprite.spritecollideany(player, enemies):
            game_over = True

    # Draw
    win.fill(BLACK)
    all_sprites.draw(win)
    text = font.render(f"Score: {score}", True, WHITE)
    win.blit(text, (10, 10))
    if game_over:
        over = font.render("GAME OVER! Press R to Restart", True, RED)
        win.blit(over, (WIDTH//2 - 200, HEIGHT//2))
    pygame.display.flip()
    clock.tick(60)
