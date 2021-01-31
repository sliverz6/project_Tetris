import pygame
import sys
import random

from settings import Settings
from game_screen import GameScreen
from block import Block
from block_data import blocks_blueprint
from score_board import ScoreBoard


def pick_block(blocks):
    """블록을 뽑아서 리스트에 순서대로 관리합니다."""
    if not blocks:  # 처음 뽑는다면?
        for _ in range(2):
            blocks.append(random.choice(blocks_blueprint))  # 2개 뽑습니다.
    else:
        next_block = blocks[1]
        blocks[0] = next_block
        blocks[1] = random.choice(blocks_blueprint)

    return blocks


def main():
    """메인 함수"""
    pygame.init()  # 설정 초기화
    settings = Settings()  # 설정 객체

    # 윈도우 생성
    window = pygame.display.set_mode((
        settings.screen_width, settings.screen_height
    ))
    pygame.display.set_caption("Tetris")  # 윈도우 타이틀 생성

    score_board = ScoreBoard(settings, window)  # 게임 점수판 객체
    game_screen = GameScreen(settings, window, score_board)  # 게임 화면 객체

    # 블록 데이터에서 하나를 뽑아서 전달.
    blocks = []
    blocks = pick_block(blocks)
    block = Block(game_screen, blocks[0])  # 블록 생성
    score_board.set_next_block(blocks[1])  # 다음 블록

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
        if drop_timer == settings.block_drop_speed:
            drop_end = block.drop()
            if drop_end:  # 바닥에 닿였다면?
                game_screen.clear_lines()  # 가득찬 줄이 있다면 지웁니다.
                blocks = pick_block(blocks)  # 블록을 뽑습니다.
                block = Block(game_screen, blocks[0])  # 블록 생성
                score_board.set_next_block(blocks[1])  # 다음 블록
            drop_timer = 0  # 낙하 타이머 초기화

        window.fill("black")
        game_screen.update()  # 게임 화면 그리기
        score_board.update()  # 게임 점수판 그리기
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
