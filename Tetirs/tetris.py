import pygame
import sys
import random

from settings import Settings
from game_screen import GameScreen
from block import Block
from block_data import blocks_blueprint


# 메인 함수
def main():
    pygame.init()  # 설정 초기화
    settings = Settings()  # 설정 객체

    # 윈도우 생성
    window = pygame.display.set_mode((
        settings.screen_width, settings.screen_height
    ))
    pygame.display.set_caption("Tetris")  # 윈도우 타이틀 생성

    game_screen = GameScreen(settings, window)  # 게임 화면 객체

    # 블록 데이터에서 하나를 뽑아서 전달.
    block_blueprint = random.choice(blocks_blueprint)
    block = Block(game_screen, block_blueprint)  # 블록 생성

    drop_timer = 0

    # 게임 메인 루프
    while True:

        # 이벤트 탐지
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    block.move("Right")
                elif event.key == pygame.K_LEFT:
                    block.move("Left")
                elif event.key == pygame.K_UP:
                    block.rotate()

        drop_timer += 1  # 블록 떨어트리기 시간
        if drop_timer == 500:
            block.drop()
            drop_timer = 0
        
        game_screen.update()  # 게임 화면 그리기
        pygame.display.update()  # 최근 화면 그리기


main()


# 2021-01-30
# TODO 1. 테트리스 화면을 만든다.
# TODO 2. 벽을 그린다.
# TODO 3. 블록을 그린다.
# TODO 4. 사용자 입력을 받아 블록을 좌,우로 움직이고 회전한다.
# TODO 5. 블록을 떨어트린다.

# 2021-01-32
# TODO 1. 블록이 벽을 통과하지 않게 한다.
# TODO 2. 블록을 쌓는다.
# TODO 3. 다 쌓인 줄을 지운다.
# TODO 4. 새로운 블록을 생성한다.
# TODO 5. 점수를 표시한다.
