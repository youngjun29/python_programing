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
        self.explosions = []
        self.running = True
        self.total_enemies = total_enemies
        self.remaining_enemies = total_enemies
        self.player_alive = True
        self.destructible_blocks = destructible_blocks
        self.time_limit = time_limit
        self.start_time = time.time()
        self.game_over = False
        self.create_walls()

    def create_walls(self):
        for _ in range(self.destructible_blocks):
            x = random.randint(0, 15) * 50
            y = random.randint(0, 11) * 50
            destructible = random.choice([True, False])
            self.walls.append(Wall(x, y, destructible))

    def start(self):
        while self.running and not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_key_input()
            self.update()
            self.update_bombs()
            self.check_time_limit()
            pygame.display.flip()
            self.clock.tick(60)

        self.quit()

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
                self.check_all_blocks_destroyed()

    def update_explosions(self):
        for explosion in self.explosions[:]:
            explosion.update()
            explosion.draw(self.screen)
            if explosion.is_finished():
                self.explosions.remove(explosion)

    def check_all_blocks_destroyed(self):
        # 파괴 가능한 블록이 모두 파괴되었는지 확인
        if all(not wall.destructible for wall in self.walls):
            print("All destructible blocks have been destroyed!")
            self.end_game(victory=True)

    def check_time_limit(self):
        # 현재 시간이 제한 시간을 초과했는지 확인
        current_time = time.time()
        if current_time - self.start_time >= self.time_limit:
            print("Time's up!")
            self.end_game()

    def end_game(self, victory=False):
        self.game_over = True
        if victory:
            print("Congratulations! You've won the game!")
        else:
            print("Game Over! Better luck next time.")

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
        if direction == 'left': new_x -= self.speed
        if direction == 'right': new_x += self.speed
        if direction == 'up': new_y -= self.speed
        if direction == 'down': new_y += self.speed
        if not self.check_collision(new_x, new_y, walls):
            self.x, self.y = max(0, min(750, new_x)), max(0, min(550, new_y))

    def check_collision(self, new_x, new_y, walls):
        player_rect = pygame.Rect(new_x, new_y, 50, 50)
        for wall in walls:
            if player_rect.colliderect(pygame.Rect(wall.x, wall.y, 50, 50)):
                return True
        return False

    def place_bomb(self, bombs):
        if len(bombs) < self.bombs_count:
            bombs.append(Bomb(self.x, self.y, timer=3))
            print(f"Bomb placed at ({self.x}, {self.y})")

class Bomb:
    def __init__(self, x, y, timer):
        self.x = x
        self.y = y
        self.timer = timer
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.font = pygame.font.Font(None, 36)

    def update(self):
        if self.timer > 0:
            self.timer -= 1 / 60

    def explode(self, walls, explosions):
        print(f"Bomb at ({self.x}, {self.y}) exploded!")
        explosions.append(Explosion(self.x, self.y, radius=1))
        self.handle_explosion(walls)

    def handle_explosion(self, walls):
        explosion_radius = 50
        explosion_area = pygame.Rect(self.x - explosion_radius, self.y - explosion_radius, 
                                     explosion_radius * 2 + 50, explosion_radius * 2 + 50)
        for wall in walls[:]:
            if explosion_area.colliderect(pygame.Rect(wall.x, wall.y, 50, 50)) and wall.destructible:
                walls.remove(wall)
                print(f"Wall at ({wall.x}, {wall.y}) destroyed by explosion!")

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        if self.timer > 0:
            screen.blit(self.font.render(str(int(self.timer)), True, (255, 255, 255)), 
                        (self.x + 10, self.y + 10))

class Explosion:
    def __init__(self, x, y, radius, duration=1):
        self.x = x
        self.y = y
        self.radius = radius
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
        self.image.fill((101, 67, 33) if destructible else (139, 69, 19))

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

# 게임 실행
game = Game(total_enemies=3, destructible_blocks=10, time_limit=120)
game.start()
