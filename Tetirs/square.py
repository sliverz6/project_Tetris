import pygame


class Square:
    """사각형 클래스"""

    def __init__(self, settings, window, y_pos, x_pos):
        """속성을 초기화합니다."""
        self.window = window  # 윈도우 객체
        self.settings = settings  # 설정 객체
        self.x_pos = x_pos  # 가로 위치
        self.y_pos = y_pos  # 세로 위치
        self.size = self.settings.square_size  # 사각형 크기
        self.filled_size = self.settings.square_filled_size  # 여백을 제외한 사각형 크기

        # rect 속성을 만듭니다.
        self.rect = pygame.Rect(self.x_pos * self.size,
                                self.y_pos * self.size,
                                self.filled_size,
                                self.filled_size)

    def fill(self, color):
        """전달 받은 스크린 데이터에 대응하는 색상으로 칠합니다."""
        pygame.draw.rect(self.window, color, self.rect)
