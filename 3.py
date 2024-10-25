import pygame

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Bomberman Game")
        self.clock = pygame.time.Clock()
        self.player = Player(50, 50, 5)  # 플레이어 초기 위치와 속도 설정
        self.bombs = []  # 게임에서 관리할 폭탄 리스트
        self.running = True

    def start(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_key_input()  # 키 입력 처리 메서드 호출
            self.update()
            self.update_bombs()  # 폭탄 상태 업데이트
            pygame.display.flip()
            self.clock.tick(60)

    def handle_key_input(self):
        """키 입력을 처리하는 메서드"""
        keys = pygame.key.get_pressed()

        # 플레이어 이동 처리
        if keys[pygame.K_LEFT]:
            self.player.move('left')
        if keys[pygame.K_RIGHT]:
            self.player.move('right')
        if keys[pygame.K_UP]:
            self.player.move('up')
        if keys[pygame.K_DOWN]:
            self.player.move('down')

        # 스페이스바로 폭탄 설치
        if keys[pygame.K_SPACE]:
            self.player.place_bomb(self.bombs)

    def update(self):
        """게임 상태를 업데이트하고 화면에 그립니다."""
        self.screen.fill((0, 0, 0))  # 화면 초기화 (검정색 배경)
        self.screen.blit(self.player.image, (self.player.x, self.player.y))  # 플레이어 그리기

        # 폭탄 그리기 및 타이머 표시
        for bomb in self.bombs:
            bomb.draw(self.screen)  # 폭탄과 타이머 그리기

    def update_bombs(self):
        """폭탄 상태를 업데이트하고 폭발 여부를 확인합니다."""
        for bomb in self.bombs[:]:  # 원본 리스트를 복사하여 반복
            bomb.update()  # 폭탄 상태 업데이트
            if bomb.timer <= 0:  # 타이머가 0 이하일 때 폭발
                bomb.explode()  # 폭발 처리
                self.bombs.remove(bomb)  # 폭탄 리스트에서 제거
                
            
    def __init__(self, total_enemies, time_limit):
        self.total_enemies = total_enemies
        self.remaining_enemies = total_enemies
        self.player_alive = True
        self.time_limit = time_limit  # 게임 시간 제한 (초)
        self.start_time = time.time()
        self.game_over = False

    def defeat_enemy(self):
        if self.remaining_enemies > 0:
            self.remaining_enemies -= 1
            print(f"Enemy defeated! {self.remaining_enemies} remaining.")
            self.check_victory()
        else:
            print("No enemies left to defeat.")

    def player_died(self):
        self.player_alive = False
        self.end_game()

    def check_victory(self):
        # 모든 적을 처치하고 플레이어가 살아 있으면 승리
        if self.remaining_enemies == 0 and self.player_alive:
            self.end_game(victory=True)

    def end_game(self, victory=False):
        self.game_over = True
        if victory:
            print("Congratulations! You've won the game!")
        else:
            print("Game Over! Better luck next time.")

    def check_time_limit(self):
        # 현재 시간이 제한 시간을 초과했는지 확인
        current_time = time.time()
        if current_time - self.start_time >= self.time_limit:
            print("Time's up!")
            self.end_game()
                
                
                
                
                
                
                
                
                

    def quit(self):
        pygame.quit()

class Player:
    def __init__(self, x, y, speed):
        self.x = x  # 플레이어의 x 좌표
        self.y = y  # 플레이어의 y 좌표
        self.lives = 3  # 플레이어의 생명
        self.speed = speed  # 플레이어의 이동 속도
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))  # 생성한 Surface(플레이어)를 파란색으로 채움
        self.bombs_count = 1  # 플레이어가 설치할 수 있는 폭탄 개수

    def move(self, direction):
        match direction:
            case 'left':
                self.x -= self.speed
            case 'right':
                self.x += self.speed
            case 'up':
                self.y -= self.speed
            case 'down':
                self.y += self.speed
            case _:
                pass

    def place_bomb(self, bombs):
        if len(bombs) < self.bombs_count:  # 설치할 수 있는 폭탄 개수 제한
            bomb = Bomb(self.x, self.y, timer=3)  # 3초 타이머로 폭탄 생성
            bombs.append(bomb)
            print(f"Bomb placed at ({self.x}, {self.y})")  # 콘솔에 폭탄 설치 위치 출력

class Bomb:  # 폭탄 클래스 시작
    def __init__(self, x, y, timer):
        self.x = x
        self.y = y
        self.timer = timer  # 폭탄 타이머 (초)
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))  # 빨간색 폭탄
        self.font = pygame.font.Font(None, 36)  # 폰트 설정

    def update(self):
        if self.timer > 0:
            self.timer -= 1 / 60  # 프레임마다 1/60초 감소

    def explode(self):
        print(f"Bomb at ({self.x}, {self.y}) exploded!")  # 폭발 위치를 화면에 출력
        # 여기에 폭발 효과 추후 추가 가능

    def draw(self, screen):
        # 폭탄 그리기
        screen.blit(self.image, (self.x, self.y))

        # 타이머 텍스트
        if self.timer > 0:
            timer_text = self.font.render(str(int(self.timer)), True, (255, 255, 255))  # 흰색 텍스트
            text_rect = timer_text.get_rect(center=(self.x + 15, self.y + 15))  # 폭탄 중앙에 텍스트 위치
            screen.blit(timer_text, text_rect)  # 화면에 타이머 텍스트 그리기

class Wall:
    def __init__(self, x, y, destructible):
        self.x = x
        self.y = y
        self.destructible = destructible

class Item:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type

    def apply_effect(self, player):
        # 아이템 효과 적용
        pass

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def place_element(self, element, x, y):
        # 보드에 요소 배치
        pass

    def remove_element(self, x, y):
        # 보드에서 요소 제거
        pass

class Explosion:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def affect_elements(self):
        # 폭발 효과 처리
        pass

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        # 적 이동 처리
        pass

    def die(self):
        # 적 사망 처리
        pass

# 게임 실행
game = Game()
game.start()
game.quit()