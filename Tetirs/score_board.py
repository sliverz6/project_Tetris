import pygame

from square import Square


class ScoreBoard:
    """게임 점수판"""

    def __init__(self, settings, window):
        """초기화"""
        self.window = window  # 윈도우 객체
        self.settings = settings  # 설정 객체
        self.score = 0  # 점수
        self.high_score = self.get_high_score_record()

        # 다음 블록 스크린
        self.next_screen_data = self.settings.next_block_screen_data
        self.next_screen_squares = self.get_next_screen_squares()
        self.next_squares_screen_data = 0

        # 텍스트 초기화
        self.score_font = pygame.font.SysFont("Arial", 25, False, False)
        self.score_text_pos = [400, 80]
        self.score_value_font = pygame.font.SysFont("Arial", 30, False, False)
        self.score_value_text_pos = [400, 120]
        self.high_score_font = pygame.font.SysFont("Arial", 25, False, False)
        self.high_score_text_pos = [400, 40]
        self.next_font = pygame.font.SysFont("Arial", 25, False, False)
        self.next_text_pos = [400, 200]

        self.score_text = self.score_font.render("Score:", True, (255, 255, 255))
        self.high_score_text = self.high_score_font.render("High Score", True, (255, 255, 255))
        self.score_value_text = self.score_value_font.render(f"{self.score}", True, (245, 194, 10))
        self.next_text = self.next_font.render("Next:", True, (255, 255, 255))

    def get_high_score_record(self):
        """저장된 최고 점수를 가져옵니다. 없다면 새로 만듭니다."""
        try:
            with open("score") as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0
            with open("score", "w") as file:
                file.write(str(self.high_score))

        return self.high_score

    def get_score(self):
        """득점합니다."""
        self.score += 100
        if self.score > self.high_score:
            self.high_score = self.score
        self.score_value_text = self.score_value_font.render(f"{self.score}", True, (245, 194, 10))

    def get_next_screen_squares(self):
        """다음 블록 스크린 데이터에 대응하는 사각형 객체 리스트를 만듭니다."""
        squares = []
        for y in range(len(self.next_screen_data)):
            for x in range(len(self.next_screen_data[0])):
                next_screen_x_pos = x + 14
                next_screen_y_pos = y + 8
                square = Square(self.settings, self.window, next_screen_y_pos, next_screen_x_pos)
                squares.append(square)  # 리스트에 추가
        return squares

    def get_color(self, y, x):
        """전달 받은 위치의 화면 데이터에 해당하는 색상을 리턴합니다."""
        scr_data = self.next_screen_data[y][x]
        return self.settings.square_colors[scr_data]

    def get_squares_position(self, block_blueprint):
        """
        블록 설계도를 전달 받아 게임 화면에 해당하는 위치 리스트로 반환합니다.
        위치는 self.block_anchor_point 에 저장된 위치를 좌상단 꼭지점으로 기준 삼아 계산됩니다.
        반환 예시) [[0, 5], [0, 6], [1, 6], [1, 7]]
        """
        pos = []
        for y in range(len(block_blueprint)):
            for x in range(len(block_blueprint[0])):
                screen_data = block_blueprint[y][x]  # 도면에 적힌 화면 데이터
                if screen_data != 0:
                    self.next_squares_screen_data = screen_data
                    new_pos = [y, x]
                    pos.append(new_pos)

        return pos

    def set_next_block(self, next_block_blueprint):
        """다음 블록 데이터를 전달해서 저장한다."""
        # 먼저 스크린 데이터를 초기화 합니다.
        for y in range(len(self.next_screen_data)):
            for x in range(len(self.next_screen_data[0])):
                self.next_screen_data[y][x] = 0  # 검정으로

        # 스크린 데이터에 블록 데이터를 업데이트합니다.
        block_pos = self.get_squares_position(next_block_blueprint[0])
        for pos in block_pos:
            self.set_screen_data(pos[0], pos[1], self.next_squares_screen_data)

    def set_screen_data(self, y, x, scr_data):
        """전달받은 위치에 화면 데이터를 설정합니다."""
        self.next_screen_data[y][x] = scr_data

    def update(self):
        """텍스트를 화면에 그립니다."""
        self.window.blit(self.score_text, self.score_text_pos)
        # self.window.blit(self.high_score_text, self.high_score_text_pos)
        self.window.blit(self.score_value_text, self.score_value_text_pos)
        self.window.blit(self.next_text, self.next_text_pos)

        for y in range(len(self.next_screen_data)):
            for x in range(len(self.next_screen_data[0])):
                color = self.get_color(y, x)  # 스크린 데이터에 해당하는 색상
                square_index = y * 4 + x  # 해당 사각형 인덱스 구하기
                self.next_screen_squares[square_index].fill(color)  # 사각형 칠하기
