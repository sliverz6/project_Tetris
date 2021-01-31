from square import Square


class GameScreen:
    """
    게임 화면 클래스입니다. 숫자로 이루어진 게임 화면 데이터(2차원 리스트)로 화면에 그려질 내용을 관리합니다.
    """

    def __init__(self, settings, window, score_board):
        """속성을 초기화합니다."""
        self.window = window  # 윈도우 객체
        self.settings = settings  # 설정 객체
        self.score_board = score_board  # 게임 점수판 객체
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

    def drop_all_line(self, row):
        """전달 받은 행 번호 위의 모든 줄을 한 칸씩 아래로 내립니다."""
        for y in range(row, 0, -1):  # 19~1
            self.screen_data[y] = self.screen_data[y-1][:]

    def clear_line(self, row):
        """전달 받은 행 번호의 줄을 지웁니다."""
        for x in range(1, len(self.screen_data[row])-1):
            self.screen_data[row][x] = 0  # 해당 줄의 스크린 데이터를 0으로 합니다.
        self.score_board.get_score()  # 득점합니다.

    def clear_lines(self):
        """가득찬 줄이 있다면 지웁니다."""
        # 가득찬 줄의 행 번호를 구합니다.
        full_line_rows = []
        for idx, row in enumerate(self.screen_data[:-1]):
            if 0 not in row[1:-1]:
                full_line_rows.append(idx)  # 행 번호를 추가합니다.

        if full_line_rows:  # 가득찬 줄이 있다면?
            full_line_rows.reverse()  # 아래에서 부터
            for row in full_line_rows:
                self.clear_line(row)  # 해당 줄을 지웁니다.
                self.drop_all_line(row)  # 위의 모든 줄을 한 칸 내립니다.
