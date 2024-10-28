import pygame
import random
import time

pygame.init()

class Game:
    def __init__(self, total_enemies, destructible_blocks, time_limit):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Bomberman Game")
        self.clock = pygame.time.Clock()
        self.player = Player(50, 50, 5)
        self.bombs = []
        self.walls = []
        self.explosions = []  # 폭발 리스트 추가
        self.running = True
        self.create_walls()

        self.total_enemies = total_enemies
        self.remaining_enemies = total_enemies
        self.player_alive = True
        self.destructible_blocks = destructible_blocks  # 파괴 가능한 블록 수
        self.time_limit = time_limit  # 게임 시간 제한 (초)
        self.start_time = time.time()
        self.game_over = False

    def create_walls(self):
        for _ in range(10):
            x = random.randint(0, 15) * 50
            y = random.randint(0, 11) * 50
            destructible = random.choice([True, False])
            self.walls.append(Wall(x, y, destructible))

    def defeat_enemy(self):
        if self.remaining_enemies > 0:
            self.remaining_enemies -= 1
            print(f"Enemy defeated! {self.remaining_enemies} remaining.")
            self.check_victory()
        else:
            print("No enemies left to defeat.")

    def destroy_block(self):
        if self.destructible_blocks > 0:
            self.destructible_blocks -= 1
            print(f"Block destroyed! {self.destructible_blocks} destructible blocks remaining.")
            self.check_all_blocks_destroyed()
        else:
            print("No destructible blocks left to destroy.")

    def check_victory(self):
        if self.remaining_enemies == 0 and self.player_alive:
            self.end_game(victory=True)

    def check_all_blocks_destroyed(self):
        if self.destructible_blocks == 0:
            print("All destructible blocks have been destroyed!")
            self.end_game(victory=True)

    def end_game(self, victory=False):
        self.game_over = True
        self.running = False
        if victory:
            print("Congratulations! You've won the game!")
        else:
            print("Game Over! Better luck next time.")

    def check_time_limit(self):
        current_time = time.time()
        if current_time - self.start_time >= self.time_limit:
            print("Time's up!")
            self.end_game()

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_key_input()
            self.update()
            self.update_bombs()
            self.check_time_limit()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_key_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move('left', self.walls)
        if keys[pygame.K_RIGHT]:
            self.player.move('right', self.walls)
        if keys[pygame.K_UP]:
            self.player.move('up', self.walls)
        if keys[pygame.K_DOWN]:
            self.player.move('down', self.walls)
        if keys[pygame.K_SPACE]:
            self.player.place_bomb(self.bombs)

    def update(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.player.image, (self.player.x, self.player.y))
        for wall in self.walls:
            wall.draw(self.screen)
        for bomb in self.bombs:
            bomb.draw(self.screen)
        self.update_explosions()

    def update_bombs(self):
        for bomb in self.bombs[:]:
            bomb.update()
            if bomb.timer <= 0:
                bomb.explode(self.walls, self.explosions)
                self.bombs.remove(bomb)

    def update_explosions(self):
        for explosion in self.explosions[:]:
            explosion.update()
            explosion.draw(self.screen)
            if explosion.is_finished():
                self.explosions.remove(explosion)

    def quit(self):
        pygame.quit()

class Player:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.lives = 3
        self.speed = speed
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.bombs_count = 1

    def move(self, direction, walls):
        new_x, new_y = self.x, self.y

        if direction == 'left':
            new_x -= self.speed
        elif direction == 'right':
            new_x += self.speed
        elif direction == 'up':
            new_y -= self.speed
        elif direction == 'down':
            new_y += self.speed

        if not self.check_collision(new_x, new_y, walls):
            if 0 <= new_x <= 800 - 50:
                self.x = new_x
            if 0 <= new_y <= 600 - 50:
                self.y = new_y

    def check_collision(self, new_x, new_y, walls):
        player_rect = pygame.Rect(new_x, new_y, 50, 50)
        for wall in walls:
            wall_rect = pygame.Rect(wall.x, wall.y, 50, 50)
            if player_rect.colliderect(wall_rect):
                return True
        return False

    def place_bomb(self, bombs):
        if len(bombs) < self.bombs_count:
            bomb = Bomb(self.x, self.y, timer=3)
            bombs.append(bomb)
            print(f"Bomb placed at ({self.x}, {self.y})")

class Bomb:
    def __init__(self, x, y, timer):
        self.x = x
        self.y = y
        self.timer = timer
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))

    def update(self):
        if self.timer > 0:
            self.timer -= 1 / 60

    def explode(self, walls, explosions):
        print(f"Bomb at ({self.x}, {self.y}) exploded!")
        explosion = Explosion(self.x, self.y, radius=1)
        explosions.append(explosion)
        self.handle_explosion(walls)

    def handle_explosion(self, walls):
        explosion_radius = 50
        explosion_area = pygame.Rect(self.x - explosion_radius, self.y - explosion_radius,
                                     explosion_radius * 2 + 50, explosion_radius * 2 + 50)

        for wall in walls[:]:
            wall_rect = pygame.Rect(wall.x, wall.y, 50, 50)
            if explosion_area.colliderect(wall_rect):
                if wall.destructible:
                    walls.remove(wall)
                    print(f"Wall at ({wall.x}, {wall.y}) destroyed by explosion!")

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Explosion:
    def __init__(self, x, y, radius, duration=1):
        self.x = x
        self.y = y
        self.radius = radius
        self.duration = duration
        self.timer = duration
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.fill((255, 165, 0, 128))

    def update(self):
        self.timer -= 1 / 60

    def draw(self, screen):
        for i in range(self.radius + 1):
            screen.blit(self.image, (self.x - i * 50, self.y))
            screen.blit(self.image, (self.x + i * 50, self.y))
            screen.blit(self.image, (self.x, self.y - i * 50))
            screen.blit(self.image, (self.x, self.y + i * 50))

    def is_finished(self):
        return self.timer <= 0

class Wall:
    def __init__(self, x, y, destructible):
        self.x = x
        self.y = y
        self.destructible = destructible
        self.image = pygame.Surface((50, 50))
        if self.destructible:
            self.image.fill((101, 67, 33))
        else:
            self.image.fill((139, 69, 19))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# 게임 실행
game = Game(total_enemies=5, destructible_blocks=10, time_limit=300)
game.start()
game.quit()