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
        for y in range(len(block_blueprint)):
            for x in range(len(block_blueprint[0])):
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

    def get_left_neighbors_pos(self):
        """좌측 사각형 옆의 좌표 리스트를 반환합니다."""
        new_pos = [[pos[0], pos[1] - 1] for pos in self.squares_position]  # 사각형들의 한 칸 왼쪽 좌표를 구합니다.
        left_neighbors_pos = []
        for pos in new_pos:
            screen_data = self.game_screen.get_screen_data(pos[0], pos[1])  # 구한 좌표의 화면 데이터를 구합니다.
            if screen_data != self.squares_screen_data:  # 해당 공간이 블록의 사각형이 있는 곳이 아니라면?
                left_neighbors_pos.append(pos)  # 이웃 좌표 리스트에 추가합니다.
        return left_neighbors_pos

    def get_right_neighbors_pos(self):
        """우측 사각형 옆의 좌표 리스트를 반환합니다."""
        new_pos = [[pos[0], pos[1]+1] for pos in self.squares_position]  # 사각형들의 한 칸 오른쪽 좌표를 구합니다.
        right_neighbors_pos = []
        for pos in new_pos:
            screen_data = self.game_screen.get_screen_data(pos[0], pos[1])  # 구한 좌표의 화면 데이터를 구합니다.
            if screen_data != self.squares_screen_data:  # 해당 공간이 블록의 사각형이 있는 곳이 아니라면?
                right_neighbors_pos.append(pos)  # 이웃 좌표 리스트에 추가합니다.
        return right_neighbors_pos

    def get_bottom_neighbors_pos(self):
        """아래 좌표 리스트를 반환합니다."""
        new_pos = [[pos[0]+1, pos[1]] for pos in self.squares_position]  # 사각형들의 한 칸 아래 좌표를 구합니다.
        bottom_neighbors_pos = []
        for pos in new_pos:
            screen_data = self.game_screen.get_screen_data(pos[0], pos[1])  # 구한 좌표의 화면 데이터를 구합니다.
            if screen_data != self.squares_screen_data:  # 해당 공간이 블록의 사각형이 있는 곳이 아니라면?
                bottom_neighbors_pos.append(pos)  # 이웃 좌표 리스트에 추가합니다.
        return bottom_neighbors_pos

    def is_empty(self, direction):
        """왼쪽 또는 오른쪽이 비었다면 True, 아니면 False 를 반환합니다."""
        is_empty = True
        neighbors_pos = None
        if direction == "Left":
            neighbors_pos = self.get_left_neighbors_pos()
        elif direction == "Right":
            neighbors_pos = self.get_right_neighbors_pos()
        elif direction == "Bottom":
            neighbors_pos = self.get_bottom_neighbors_pos()

        # 이웃 스크린 데이터를 확인합니다.
        for pos in neighbors_pos:
            screen_data = self.game_screen.get_screen_data(pos[0], pos[1])
            if screen_data != 0:
                is_empty = False

        return is_empty

    def move(self, direction):
        """블록을 왼쪽 또는 오른쪽으로 움직입니다."""
        # 방향에 따라 이동량을 정합니다.
        movement = 1
        if direction == "Left":
            movement *= -1

        # 왼쪽 또는 오른쪽으로 갈 수 있는가? - 검사
        if self.is_empty(direction):

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

        # 이전 도면을 저장해 둡니다.
        previous_block_blueprint = self.block_blueprint[self.rotate_number]

        # 회전 번호를 구합니다.
        self.rotate_number += 1
        if self.rotate_number >= len(self.block_blueprint):
            self.rotate_number = 0

        # 회전할 수 있는지 판단합니다.
        is_rotatable = True
        temp_squares_position = None

        # I자형 블록은 따로 관리합니다. I자형 블록이 세워져있고 벽에 붙어있다면?
        if len(previous_block_blueprint) == 4 and not self.is_empty("Right"):
            is_rotatable = False  # 회전 불가
        else:
            next_block_blueprint = self.block_blueprint[self.rotate_number]
            temp_squares_position = self.get_squares_position(next_block_blueprint)

            # 회전했을 경우 스크린 데이터를 확인합니다.
            for pos in temp_squares_position:
                # 해당 자리가 비어있지 않다면?
                if self.game_screen.get_screen_data(pos[0], pos[1]) == 0 or \
                        self.game_screen.get_screen_data(pos[0], pos[1]) == self.squares_screen_data:
                    continue
                else:
                    is_rotatable = False

        if is_rotatable:
            self.remove()
            self.squares_position = temp_squares_position
            self.draw()
        else:
            self.rotate_number -= 1
            return

    def drop(self):
        """블록을 아래로 한 칸 떨어트립니다."""
        if self.is_empty("Bottom"):  # 아래쪽이 비었다면?
            self.remove()

            # 위치 값을 수정합니다.
            for pos in self.squares_position:  # 모든 사각형 위치 y좌표 + 1
                pos[0] += 1
            self.block_anchor_point[0] += 1  # 기준점 y좌표 + 1

            self.draw()
        else:
            # 쌓는다.
            self.remove()
            self.squares_screen_data += 7  # 스크린 데이터를 쌓인 색으로 바꾼다.
            self.draw()  # 다시 그린다.
            return True
