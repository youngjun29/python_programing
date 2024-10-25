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