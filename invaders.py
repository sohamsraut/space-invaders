import pygame
import random
import sys

# --------- Configuration ----------
WIDTH, HEIGHT = 800, 600
FPS = 60

PLAYER_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED_X = 1.0
ENEMY_DROP = 20
ENEMY_BULLET_CHANCE = 0.002
ENEMY_ROWS = 5
ENEMY_COLS = 10
ENEMY_X_PADDING = 60
ENEMY_Y_PADDING = 40
ENEMY_START_Y = 50

BG_COLOR = (8, 8, 30)
TEXT_COLOR = (240, 240, 240)

# --------- Pygame init ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders - Pygame")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 20)

def draw_text(surf, text, x, y):
    img = font.render(text, True, TEXT_COLOR)
    surf.blit(img, (x, y))

# --------- Sprites ----------
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load custom sprite
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = PLAYER_SPEED
        self.cooldown = 0

    def update(self, keys=None):
        if keys is None:
            keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, WIDTH)
        if self.cooldown > 0:
            self.cooldown -= 1

    def shoot(self):
        if self.cooldown == 0:
            bullet = Bullet(self.rect.centerx, self.rect.top, -BULLET_SPEED, "player")
            all_sprites.add(bullet)
            player_bullets.add(bullet)
            self.cooldown = 12

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load custom sprite
        self.image = pygame.image.load("assets/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 28))
        self.rect = self.image.get_rect(topleft=(x, y))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vy, owner):
        super().__init__()
        self.image = pygame.Surface((4, 10))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect(center=(x,y))
        self.vy = vy
        self.owner = owner

    def update(self):
        self.rect.y += self.vy
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, vy):
        super().__init__()
        self.image = pygame.Surface((6, 12))
        self.image.fill((255, 200, 60))
        self.rect = self.image.get_rect(center=(x, y))
        self.vy = vy

    def update(self):
        self.rect.y += self.vy
        if self.rect.top > HEIGHT:
            self.kill()

class BarrierBlock(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((8,8))
        self.image.fill((80, 200, 120))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.health = 3

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
        else:
            shade = 80 + self.health * 40
            self.image.fill((shade, 200, 120))

# --------- Groups ----------
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
barriers = pygame.sprite.Group()

# --------- Create player ----------
player = Player(WIDTH // 2, HEIGHT - 30)
all_sprites.add(player)

# --------- Create enemies ----------
def create_enemy_wave(rows, cols):
    margin_x = (WIDTH - (cols * ENEMY_X_PADDING)) // 2
    for row in range(rows):
        for col in range(cols):
            x = margin_x + col * ENEMY_X_PADDING
            y = ENEMY_START_Y + row * ENEMY_Y_PADDING
            e = Enemy(x, y)
            all_sprites.add(e)
            enemies.add(e)

create_enemy_wave(ENEMY_ROWS, ENEMY_COLS)

# --------- Barriers ----------
def create_barriers():
    positions = [WIDTH//4, WIDTH//2, 3*WIDTH//4]
    barrier_y = HEIGHT - 140
    for pos in positions:
        for bx in range(-3, 4):
            for by in range(0, 3):
                if (abs(bx) == 3 and by == 0):
                    continue
                block = BarrierBlock(pos + bx*10, barrier_y + by*10)
                barriers.add(block)
                all_sprites.add(block)

create_barriers()

# --------- Enemy movement logic ----------
enemy_direction = 1
enemy_speed = ENEMY_SPEED_X
score = 0
level = 1
game_over = False

def advance_level():
    global enemy_speed, level, ENEMY_BULLET_CHANCE
    level += 1
    enemy_speed += 0.4
    ENEMY_BULLET_CHANCE = min(0.01, ENEMY_BULLET_CHANCE + 0.0008)

# --------- Main loop ----------
while True:
    clock.tick(FPS)

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()
            if event.key == pygame.K_r and game_over:
                # restart game
                all_sprites.empty()
                enemies.empty()
                player_bullets.empty()
                enemy_bullets.empty()
                barriers.empty()
                player = Player(WIDTH // 2, HEIGHT - 30)
                all_sprites.add(player)
                create_enemy_wave(ENEMY_ROWS, ENEMY_COLS)
                create_barriers()
                enemy_direction = 1
                enemy_speed = ENEMY_SPEED_X
                score = 0
                level = 1
                game_over = False

    if not game_over:
        keys = pygame.key.get_pressed()
        player.update(keys)

        if enemies:
            leftmost = min(e.rect.left for e in enemies)
            rightmost = max(e.rect.right for e in enemies)
            if leftmost <= 0 and enemy_direction < 0:
                enemy_direction = 1
                for e in enemies:
                    e.rect.y += ENEMY_DROP
            elif rightmost >= WIDTH and enemy_direction > 0:
                enemy_direction = -1
                for e in enemies:
                    e.rect.y += ENEMY_DROP
            else:
                for e in enemies:
                    e.rect.x += enemy_direction * enemy_speed

            for e in list(enemies):
                if random.random() < ENEMY_BULLET_CHANCE:
                    column_x = e.rect.centerx
                    same_column = [x for x in enemies if abs(x.rect.centerx - column_x) < 4]
                    lowest = max(same_column, key=lambda s: s.rect.centery)
                    if lowest is e:
                        b = EnemyBullet(e.rect.centerx, e.rect.bottom + 10, vy=4 + level*0.3)
                        all_sprites.add(b)
                        enemy_bullets.add(b)

        all_sprites.update()

        hits = pygame.sprite.groupcollide(enemies, player_bullets, True, True)
        score += len(hits) * 10

        if pygame.sprite.spritecollide(player, enemy_bullets, True):
            game_over = True

        for b in list(player_bullets) + list(enemy_bullets):
            block_hit = pygame.sprite.spritecollideany(b, barriers)
            if block_hit:
                b.kill()
                block_hit.hit()

        for e in enemies:
            if e.rect.bottom >= player.rect.top:
                game_over = True
                break

        if not enemies:
            advance_level()
            create_enemy_wave(ENEMY_ROWS, ENEMY_COLS)
            for s in list(barriers):
                s.kill()
            create_barriers()
            player.rect.centerx = WIDTH // 2

    # --- Drawing ---
    screen.fill(BG_COLOR)
    all_sprites.draw(screen)
    draw_text(screen, f"Score: {score}", 10, 10)
    draw_text(screen, f"Level: {level}", WIDTH - 110, 10)
    if game_over:
        draw_text(screen, "GAME OVER - Press R to restart or Q to quit", WIDTH//2 - 220, HEIGHT//2)
    pygame.display.flip()
