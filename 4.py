
    def __init__(self, total_enemies, destructible_blocks, time_limit):
        self.total_enemies = total_enemies
        self.remaining_enemies = total_enemies
        self.player_alive = True
        self.destructible_blocks = destructible_blocks  # 파괴 가능한 블록 수
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

    def destroy_block(self):
        if self.destructible_blocks > 0:
            self.destructible_blocks -= 1
            print(f"Block destroyed! {self.destructible_blocks} destructible blocks remaining.")
            self.check_all_blocks_destroyed()
        else:
            print("No destructible blocks left to destroy.")

    def player_died(self):
        self.player_alive = False
        self.end_game()

    def check_victory(self):
        # 모든 적을 처치하고 플레이어가 살아 있으면 승리
        if self.remaining_enemies == 0 and self.player_alive:
            self.end_game(victory=True)

    def check_all_blocks_destroyed(self):
        # 파괴 가능한 블록이 모두 파괴되었는지 확인
        if self.destructible_blocks == 0:
            print("All destructible blocks have been destroyed!")
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

    def play(self):
        while not self.game_over:
            self.check_time_limit()
            action = input("Enter 'enemy' to defeat an enemy, 'block' to destroy a block, or 'quit' to exit: ")
            if action == "enemy":
                self.defeat_enemy()
            elif action == "block":
                self.destroy_block()
            elif action == "quit":
                self.end_game()
