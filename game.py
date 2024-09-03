import pygame
from settings import screen, WIDTH, HEIGHT, FPS, BLACK, board

import sys



class Game:
    running = True
    fullBlockHeight = HEIGHT // len(board)
    fullBlockWidth = WIDTH // len(board[0])
    from player import Player
    plr = Player()
    plr.gameData["fullBlockHeight"] = fullBlockHeight
    plr.gameData["fullBlockWidth"] = fullBlockWidth

    @staticmethod
    def frame_logic():
        for event in pygame.event.get():
            event: pygame.event.Event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            Game.plr.handle_key(event)

        Game.plr.update()

    @staticmethod
    def frame_graphics():
        screen.fill(BLACK)
        Game.plr.draw_board(board)
        pygame.display.flip()


    @staticmethod
    def frame():
        Game.frame_logic()
        Game.frame_graphics()

    @staticmethod
    def run():
        while Game.running:
            Game.frame()
            pygame.time.Clock().tick(FPS)