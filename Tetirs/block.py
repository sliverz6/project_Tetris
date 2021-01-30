class Block:
    """블록 클래스"""

    def __init__(self, game_screen, block_blueprint):
        """초기화"""
        self.game_screen = game_screen  # 게임 화면 객체
        self.block_blueprint = block_blueprint  # 블록 도면

        self.rotate_number = 0  # 회전 번호
        self.block_anchor_point = [0, 5]  # 블록 기준 좌표

        initial_block_blueprint = self.block_blueprint[self.rotate_number]  # 회전 번호 0인 블록 도면
        self.squares_screen_data = 0
        self.squares_position = self.get_squares_position(initial_block_blueprint)

        # 블록 그리기
        self.draw()

    def get_squares_position(self, block_blueprint):
        """
        블록 설계도를 전달 받아 게임 화면에 해당하는 위치 리스트로 반환합니다.
        위치는 self.block_anchor_point 에 저장된 위치를 좌상단 꼭지점으로 기준 삼아 계산됩니다.
        반환 예시) [[0, 5], [0, 6], [1, 6], [1, 7]]
        """
        pos = []
        for y in range(len(block_blueprint)):  # 3
            for x in range(len(block_blueprint[0])):  # 2
                screen_data = block_blueprint[y][x]  # 도면에 적힌 화면 데이터
                if screen_data != 0:
                    self.squares_screen_data = screen_data
                    new_pos = [y + self.block_anchor_point[0], x + self.block_anchor_point[1]]
                    pos.append(new_pos)

        return pos

    def draw(self):
        """블록을 그립니다."""
        for pos in self.squares_position:
            self.game_screen.set_screen_data(pos[0], pos[1], self.squares_screen_data)

    def remove(self):
        """블록을 지웁니다."""
        for pos in self.squares_position:
            self.game_screen.set_screen_data(pos[0], pos[1], 0)

    def move(self, direction):
        """블록을 왼쪽 또는 오른쪽으로 움직입니다."""
        # 방향에 따라 이동량을 정합니다.
        movement = 1
        if direction == "Left":
            movement *= -1

        # 블록을 지웁니다.
        self.remove()

        # 위치 값을 수정합니다.
        for pos in self.squares_position:  # 모든 사각형 x좌표 변형
            pos[1] += movement
        self.block_anchor_point[1] += movement  # 기준점 x좌표 변형

        # 블록을 그립니다.
        self.draw()

    def rotate(self):
        """블록을 회전합니다."""
        self.remove()

        # 회전 번호를 구합니다.
        self.rotate_number += 1
        if self.rotate_number >= len(self.block_blueprint):
            self.rotate_number = 0

        # 새로운 블록 도면을 갖고 위치값을 얻습니다.
        next_block_blueprint = self.block_blueprint[self.rotate_number]
        self.squares_position = self.get_squares_position(next_block_blueprint)

        # 블록을 그립니다.
        self.draw()

    def drop(self):
        """블록을 아래로 한 칸 떨어트립니다."""
        self.remove()

        # 위치 값을 수정합니다.
        for pos in self.squares_position:  # 모든 사각형 위치 y좌표 + 1
            pos[0] += 1
        self.block_anchor_point[0] += 1  # 기준점 y좌표 + 1

        self.draw()
