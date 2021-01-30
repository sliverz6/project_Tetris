from square import Square


class GameScreen:
    """
    게임 화면 클래스입니다. 숫자로 이루어진 게임 화면 데이터(2차원 리스트)로 화면에 그려질 내용을 관리합니다.
    """

    def __init__(self, settings, window):
        """속성을 초기화합니다."""
        self.window = window  # 윈도우 객체
        self.settings = settings  # 설정 객체
        self.screen_data = self.settings.screen_data  # 게임 화면 데이터
        self.screen_squares = self.get_screen_squares()  # 화면 데이터에 해당하는 사각형 리스트를 받습니다.

    def get_screen_squares(self):
        """게임 화면 데이터에 대응하는 사각형 객체 리스트를 만듭니다."""
        squares = []
        for y in range(len(self.screen_data)):
            for x in range(len(self.screen_data[0])):
                square = Square(self.settings, self.window, y, x)
                squares.append(square)  # 리스트에 추가
        return squares

    def set_screen_data(self, y, x, scr_data):
        """전달받은 위치에 화면 데이터를 설정합니다."""
        self.screen_data[y][x] = scr_data

    def get_screen_data(self, y, x):
        """전달 받은 위치의 화면 데이터를 리턴합니다."""
        return self.screen_data[y][x]

    def get_color(self, y, x):
        """전달 받은 위치의 화면 데이터에 해당하는 색상을 리턴합니다."""
        scr_data = self.screen_data[y][x]
        return self.settings.square_colors[scr_data]

    def update(self):
        """게임 화면을 새로 그립니다."""
        for y in range(len(self.screen_data)):
            for x in range(len(self.screen_data[0])):
                color = self.get_color(y, x)  # 스크린 데이터에 해당하는 색상
                square_index = y * 12 + x  # 해당 사각형 인덱스 구하기
                self.screen_squares[square_index].fill(color)  # 사각형 칠하기
